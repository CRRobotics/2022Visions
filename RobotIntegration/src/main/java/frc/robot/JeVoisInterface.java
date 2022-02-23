package frc.robot;

import edu.wpi.first.cscore.MjpegServer;
import edu.wpi.first.cscore.UsbCamera;
import edu.wpi.first.cscore.VideoMode.PixelFormat;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.SerialPort;
import edu.wpi.first.wpilibj.Timer;

import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableEntry;
import edu.wpi.first.networktables.NetworkTableInstance;


public class JeVoisInterface {
    
    // Serial Port Constants 
    private static final int BAUD_RATE = 38400;
    
    // MJPG Streaming Constants 
    private static final int MJPG_STREAM_PORT = 1180;
    
    // Packet format constants 
    private static final String PKT_START = "{";
    private static final String PKT_END = "}";
    private static final String PKT_SEP = " ";
    
    // Serial port used for getting target data from JeVois 
    private SerialPort visionPort = null;
    
    // USBCam and server used for broadcasting a webstream of what is seen 
    private UsbCamera visionCam = null;
    private MjpegServer camServer = null;
    
    // Status variables 
    private boolean dataStreamRunning = false;
    private boolean visionOnline = false;
   
    private Double[] positionRed = { 0.0, 0.0 };
    private Double[] positionBlue = { 0.0, 0.0 };
    private Integer frameNo = 0;
    
    // Packet rate performace tracking
    private double packetRxTime = 0;
    private double prevPacketRxTime = 0;
    private double packetRate_PPS = 0;
    private double packetRxRatePPS = 0;


    //=======================================================
    //== BEGIN PUBLIC INTERFACE
    //=======================================================

    /**
     * Constructor (simple). Opens a USB serial port to the JeVois camera, sends a few test commands checking for error,
     * then fires up the user's program and begins listening for target info packets in the background
     */
    public JeVoisInterface() {
        this(false); //Default - stream disabled, just run serial.

        positionRed = new Double[2];
        positionBlue = new Double[2]; 
    }

    /**
     * Constructor (more complex). Opens a USB serial port to the JeVois camera, sends a few test commands checking for error,
     * then fires up the user's program and begins listening for target info packets in the background.
     * Pass TRUE to additionaly enable a USB camera stream of what the vision camera is seeing.
     */
    public JeVoisInterface(boolean useUSBStream) {
        int retry_counter = 0;
        
        //Retry strategy to get this serial port open.
        //I have yet to see a single retry used assuming the camera is plugged in
        // but you never know.
        while(visionPort == null && retry_counter++ < 10){
            try {
                System.out.print("Creating JeVois SerialPort...");
                visionPort = new SerialPort(BAUD_RATE, SerialPort.Port.kMXP);
                System.out.println("SUCCESS!!");
            } catch (Exception e) {
                System.out.println("FAILED!!");
                e.printStackTrace();
                sleep(500);
                System.out.println("Retry " + Integer.toString(retry_counter));
            }
        }

        
        //Report an error if we didn't get to open the serial port
        if (visionPort == null){
            DriverStation.reportError("Cannot open serial port to JeVois. Not starting vision system.", false);
            return;
        }
        
        //Test to make sure we are actually talking to the JeVois
        if (sendPing() != 0){
            DriverStation.reportError("JeVois ping test failed. Continuing anyway.", false);
            //return;
        }

        start();

        //Start listening for packets
        packetListenerThread.setDaemon(true);
        packetListenerThread.start();

    } 

    public void start(){
            // Deferring DataOnlyStream until we enter Teleop
            startDataOnlyStream();
            System.out.println("Starting DataOnlyStream\n");
    }

    public void stop(){
        stopDataOnlyStream();
    }
    
    public boolean isVisionOnline() {
        return visionOnline;
    }

    
    //=======================================================
    //== END PUBLIC INTERFACE
    //=======================================================
    
    /**
     * This is the main perodic update function for the Listener. It is intended
     * to be run in a background task, as it will block until it gets packets. 
     */

    private int throttle = 0;

    private void backgroundUpdate(){
        // Grab packets and parse them.
        String packet;
        
        packet = blockAndGetPacket(2.0);

        if (packet != null){
            packetRxTime = Timer.getFPGATimestamp();

            if (parsePacket(packet, packetRxTime) == 0){
                visionOnline = true;
                packetRxRatePPS = 1.0/(packetRxTime - prevPacketRxTime);

                if (true) {
                    System.out.print("gpkt fr " + frameNo.toString() + " blue pos " + positionBlue[0].toString());
                    System.out.print(" blue ang  " + positionBlue[1].toString() + " red pos " + positionRed[0].toString());
                    System.out.println(" red ang " + positionRed[1].toString());
                }

                NetworkTableInstance inst = NetworkTableInstance.getDefault();
                NetworkTable table = inst.getTable("visions");
        
                NetworkTableEntry entry = table.getEntry("blueDist");
                entry.setDouble(positionBlue[0]);
                
                entry = table.getEntry("blueAngle");
                entry.setDouble(positionBlue[1]);
                
                entry = table.getEntry("redDist");
                entry.setDouble(positionRed[0]);
                
                entry = table.getEntry("redAngle");
                entry.setDouble(positionRed[1]);
            } else {
                visionOnline = false;
            }
            
        } else {
            visionOnline = false;
            // DriverStation.reportWarning("No packet received (bg)", false);
        }
    }

    /**
     * Send the ping command to the JeVois to verify it is connected
     * @return 0 on success, -1 on unexpected response, -2 on timeout
     */
    private int sendPing() {
        int retval = -1;
        if (visionPort != null){
            // System.out.print("Sending PING\n");
            retval = sendCmdAndCheck("ping");
        } else {
            // System.out.print("Serial port NULL; not sending\n");
        }
        return retval;
    }

    private void startDataOnlyStream() {
        dataStreamRunning = true;
        //sendCmd("streamon");
        System.out.println("JeVois send streamon");
    }

    private void stopDataOnlyStream() {
        //sendCmd("streamoff");
        System.out.println("JeVois send streamoff");
    }

    
    /**
     * Sends a command over serial to JeVois and returns immediately.
     * @param cmd String of the command to send (ex: "ping")
     * @return number of bytes written
     */
    public int sendCmd(String cmd){
        int bytes;
        bytes = visionPort.writeString(cmd + "\n");
        return bytes;
    };
    
    /**
     * Sends a command over serial to the JeVois, waits for a response, and checks that response
     * Automatically ends the line termination character.
     * @param cmd String of the command to send (ex: "ping")
     * @return 0 if OK detected, -1 if ERR detected, -2 if timeout waiting for response
     */
    public int sendCmdAndCheck(String cmd){
        int retval = 0;
        sendCmd(cmd);
        retval = blockAndCheckForOK(1.0);
        if (retval == -1) {
            System.out.println(cmd + " Produced an error");
        } else if (retval == -2) {
            System.out.println(cmd + " timed out");
        }
        return retval;
    };

    //Persistent but "local" variables for getBytesPeriodic()
    private String getBytesWork = "";
    private int loopCount = 0;
    /**
     * Read bytes from the serial port in a non-blocking fashion
     * Will return the whole thing once the first "OK" or "ERR" is seen in the stream.
     * Returns null if no string read back yet.
     */
    private String getCmdResponseNonBlock() {
        String retval =  null;
        if (visionPort != null){
            if (visionPort.getBytesReceived() > 0) {
                String rxString = visionPort.readString();
                System.out.println("Waited: " + loopCount + " loops, Rcv'd: " + rxString);
                getBytesWork += rxString;
                if(getBytesWork.contains("OK") || getBytesWork.contains("ERR")){
                    retval = getBytesWork;
                    getBytesWork = "";
                    System.out.println(retval);
                }
                loopCount = 0;
            } else {
                ++loopCount;
            }
        }
        return retval;
    }
    
    /** 
     * Blocks thread execution till we get a response from the serial line
     * or timeout. 
     * Return values:
     *  0 = OK in response
     * -1 = ERR in response
     * -2 = No token found before timeout_s
     */
    private int blockAndCheckForOK(double timeout_s){
        int retval = -2;
        double startTime = Timer.getFPGATimestamp();
        String testStr = "";
        if (visionPort != null){
            while(Timer.getFPGATimestamp() - startTime < timeout_s){
                if (visionPort.getBytesReceived() > 0) {
                    testStr += visionPort.readString();
                    if(testStr.contains("OK")){
                        retval = 0;
                        break;
                    }else if(testStr.contains("ERR")){
                    	DriverStation.reportError("JeVois reported error:\n" + testStr, false);
                        retval = -1;
                        break;
                    }

                } else {
                    sleep(10);
                }
            }
        }
        return retval;
    }
    
    
    // buffer to contain data from the port while we gather full packets 
    private StringBuffer packetBuffer = new StringBuffer(100);
    /** 
     * Blocks thread execution till we get a valid packet from the serial line
     * or timeout. 
     * Return values:
     *  String = the packet 
     *  null = No full packet found before timeout_s
     */
    private String blockAndGetPacket(double timeout_s){
        String retval = null;
        double startTime = Timer.getFPGATimestamp();
        int endIdx = -1;
        int startIdx = -1;
        
        if (visionPort != null) {
            while (Timer.getFPGATimestamp() - startTime < timeout_s){
                // Keep trying to get bytes from the serial port until the timeout expires.
                if (visionPort.getBytesReceived() > 0) {
                    // If there are any bytes available, read them in and 
                    //  append them to the buffer.
                	packetBuffer = packetBuffer.append(visionPort.readString());

                    // Attempt to detect if the buffer currently contains a complete packet
                    if (packetBuffer.indexOf(PKT_START) != -1){
                    	endIdx = packetBuffer.lastIndexOf(PKT_END);
                        if (endIdx != -1){
                            // Buffer also contains at least one start & end character.
                            // But we don't know if they're in the right order yet.
                            // Start by getting the most-recent packet end character's index
                             
                            
                            // Look for the index of the start character for the packet
                            //  described by endIdx. Note this line of code assumes the 
                            //  start character for the packet must come _before_ the
                            //  end character.
                            startIdx = packetBuffer.lastIndexOf(PKT_START, endIdx);
                            
                            if (startIdx == -1){
                                // If there was no start character before the end character,
                                //  we can assume that we have something a bit wacky in our
                                //  buffer. For example: ",abc}garbage{1,2".
                                // Since we've started to receive a good packet, discard 
                                //  everything prior to the start character.
                                startIdx = packetBuffer.lastIndexOf(PKT_START);
                                packetBuffer.delete(0, startIdx);
                            } else {
                                // Buffer contains a full packet. Extract it and clean up buffer
                                retval = packetBuffer.substring(startIdx+1, endIdx-1);
                                packetBuffer.delete(0, endIdx+1);
                                break;
                            } 
                        } else {
                          // In this case, we have a start character, but no end to the buffer yet. 
                          //  Do nothing, just wait for more characters to come in.
                          sleep(5);
                        }
                    } else {
                        // Buffer contains no start characters. None of the current buffer contents can 
                        //  be meaningful. Discard the whole thing.
                        packetBuffer.delete(0, packetBuffer.length());
                        sleep(5);
                    }
                } else {
                    sleep(5);
                }
            }
        }
        return retval;
    }
    
    /**
     * Private wrapper around the Thread.sleep method, to catch that interrupted error.
     * @param time_ms
     */
    private void sleep(int time_ms){
        try {
            Thread.sleep(time_ms);
        } catch (InterruptedException e) {
            System.out.println("DO NOT WAKE THE SLEEPY BEAST");
            e.printStackTrace();
        }
    }
    
    /**
     * Mostly for debugging. Blocks execution forever and just prints all serial 
     * characters to the console. It might print a different message too if nothing
     * comes in.
     */
    public void blockAndPrintAllSerial(){
        if (visionPort != null){
            while(!Thread.interrupted()){
                if (visionPort.getBytesReceived() > 0) {
                    System.out.print(visionPort.readString());
                } else {
                    System.out.println("Nothing Rx'ed");
                    sleep(100);
                }
            }
        }

    }


    /**
     * Parse individual numbers from a packet
     * @param pkt
     */
    public int parsePacket(String pkt, double rx_Time){
        //Parsing constants. These must be aligned with JeVois code.

        // Fields:
        // 0 : frameno <integer>
        // 1 : red ball distance (inches) <<float>>
        // 2 : red ball angle (radians) <<float>>
        // 3 : blue ball distance <<float>>
        // 4 : blue ball angle <<float>> 

		final int NTOK = 5;
		final int TOK_FRAME_CNT = 0;
        final int TOK_BLUE_ANGLE = 1;
        final int TOK_BLUE_DIST = 2;
        final int TOK_RED_ANGLE = 3;
        final int TOK_RED_DIST = 4;
 

        
        //Split string into many substrings, presuming those strings are separated by commas
        String[] tokens = pkt.split(PKT_SEP);
        //System.out.println("RAW pkt:" + pkt);

        int rc = 0;
        Integer tokidx = 0, state = 0;
        while (tokidx < tokens.length) {
            try { 
                if (tokens[tokidx].length() < 1) {
                    // System.out.println("zero len token at " + tokidx.toString());
                } else {
                    // System.out.println("Parsing token " + tokens[tokidx]);

                    if (state == TOK_FRAME_CNT) {
                        frameNo = Integer.parseInt(tokens[tokidx]);
                    } else if (state == TOK_RED_DIST) {
                        positionRed[0] = Double.parseDouble(tokens[tokidx]);
                    } else if (state == TOK_RED_ANGLE) {
                        positionRed[1] = Double.parseDouble(tokens[tokidx]);
                    } else if (state == TOK_BLUE_DIST) {
                        positionBlue[0] = Double.parseDouble(tokens[tokidx]);
                    } else if (state == TOK_BLUE_ANGLE) {
                        positionBlue[1] = Double.parseDouble(tokens[tokidx]);
                    } else {
                        // System.out.println("igoring trailing token " + tokens[tokidx]+ " " + tokidx.toString());
                    }
                    state += 1;
                }
                tokidx += 1;
            } catch (Exception e) {
                System.out.println("++++++++++++++++++++++++ ERR parsing packet +++++++++++++++++++++++++");
                e.printStackTrace();
                System.out.println("tokidx " + tokidx.toString() + " value " + tokens[tokidx]);
                positionRed[0] = -1.0; positionRed[1] = -1.0;
                rc = -1;
            }   
        }         
        return rc;   
    }
    
    
    /**
     * This thread runs a periodic task in the background to listen for vision camera packets.
     */
    Thread packetListenerThread = new Thread(new Runnable() {
        public void run() {
        	while(!Thread.interrupted()){
        		backgroundUpdate();   
        	}
        }
    });
    
}
