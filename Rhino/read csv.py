import rhinoscriptsyntax as rs

file = r"C:\Users\mkreidler\Desktop\points_in_zones.csv"

block_zones = []

with open(file, "r") as f:
    for i, line in enumerate(f):
        # don't look at header row
        if i != 0:
            block = line.strip().split(',')[0]
            zone = line.strip().split(',')[1]
            
            temp = {block:zone}
            
