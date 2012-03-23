lines = open("/proc/net/dev", "r").readlines()

columnLine = lines[1]
_, receiveCols , transmitCols = columnLine.split("|")
receiveCols = map(lambda a:"recv_"+a, receiveCols.split())
transmitCols = map(lambda a:"trans_"+a, transmitCols.split())

cols = receiveCols+transmitCols

faces = {}
for line in lines[2:]:
    if line.find(":") < 0: continue
    face, data = line.split(":")
    faceData = dict(zip(cols, data.split()))
    faces[face.strip()] = faceData

import pprint
pprint.pprint(faces)
