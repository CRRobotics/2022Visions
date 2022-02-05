import functions
jsonMSG = """
{
    r : [15,3]
    b : [15,2]
    h : [12, 8]
}
"""

print(functions.findChecksum(jsonMSG))