x = 0.0
y = 0.0
z = 0.0
yaw = 0.0
recording = False
frecord = True
recordcomplete = False
landing = False
touchFlag = False
mapX = 0.0
mapY = 0.0
reconnect = False

def operate(code):
    global x, y, z, yaw, recording, frecord, landing, touchFlag, mapX, mapY
    frecord = recording
    x = code['dx']
    y = code['dy']
    z = code['dz']
    yaw = code['dyaw']
    recording = code['record']
    landing = code['land']
    touchFlag = code['pointFlag']
    mapX = code['pointX']
    mapY = code['pointY']
    reconnect = code['reconnect']

    print(f"{x} {y} {z} {yaw} {recording} {landing} {touchFlag} {mapX} {mapY} {reconnect}")