import socket
import numpy as np
import json
import time
import random
import drone
import control

testArray = []
testpathArray = []

mCount = 5
"""
for i in range(1, 1000) :
    testArray.append(0)
    testArray.append(i * 0.1)

for i in range(1, 1000) :
    testArray.append(i * 0.1)
    testArray.append(0)

for i in range(1, 1000) :
    testArray.append(i * 0.1)
    testArray.append(100)

for i in range(1, 1000) :
    testArray.append(100)
    testArray.append(i * 0.1)

"""

for i in range(1, 21):
    testpathArray.append(0.5)
    testpathArray.append(0.5 + 0.025 * i)
    testpathArray.append(0.5)

"""

for i in range(1, 100):
    for j in range(1, 100):
        testpathArray.append(i * 1)
        testpathArray.append(j * 1)
        """


def followTouch() :
    while True:
        touchedX = control.mapX
        touchedY = control.mapY
        drone.x += (touchedX - drone.x) * 0.01
        drone.y += (touchedY - drone.y) * 0.01
        time.sleep(0.02)


def ramdomPoint():
    global testArray
    while True:
        testArray.clear()
        for _ in range(500000):
            x = random.uniform(0, 2)  # x 좌표
            y = random.uniform(0, 2)  # y 좌표
            z = random.uniform(0, 2)  # z 좌표
            testArray.extend([x, y, z])  # 배열에 x, y, z 순서로 추가
        time.sleep(1)


for i in range(500):
    testArray.append(i)
    testArray.append(0)

for i in range(500):
    testArray.append(0)
    testArray.append(i)

for i in range(500):
    testArray.append(i)
    testArray.append(500)

for i in range(500):
    testArray.append(500)
    testArray.append(i)


for i in range(500):
    for j in range(500):
        testpathArray.append(i)
        testpathArray.append(j)