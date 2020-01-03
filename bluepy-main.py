from bluepy.btle import Scanner, DefaultDelegate, Peripheral, UUID, BTLEException, Service, Characteristic
import string
import ctypes
import binascii

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy
import math

vertices = (
    (2.5, -0.7, -3.35),
    (2.5, 0.7, -3.35),
    (-2.5, 0.7, -3.35),
    (-2.5, -0.7, -3.35),
    (2.5, -0.7, 3.35),
    (2.5, 0.7, 3.35),
    (-2.5, -0.7, 3.35),
    (-2.5, 0.7, 3.35),
    )

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
    )

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
    )

colors = (
    (1,0,0),
    (1,1,0),
    (1,0,1),
    (1,0,0),
    (1,0,0),
    (1,0,1),
    (1,1,0),
    (1,0,1),
    (0,0,1),
    (1,0,0),
    (1,0,1),
    (0,0,1)
    )

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

#   def handleDiscovery(self, dev, isNewDev, isNewData):
#        if isNewDev:
#            print ("Discovered device", dev.addr)
#        elif isNewData:
#            print ("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(3)

#my keyboard:"88:c6:26:ba:42:85"
#10 = indoor positioning service
#24:71:89:09:90:84

def hexToSignedInt(hexValue):
    # v convert from hex to byte
    byteValue = bytes(hexValue, 'utf-8')
    byteValue = binascii.a2b_hex(byteValue)
    # v convert from byte to integer
    intValue = int.from_bytes(byteValue, byteorder='little', signed=True)

    return intValue

def Cube():
    glBegin(GL_QUADS)
    index = 0
    for surface in surfaces:
        glColor3fv(colors[index])
        index += 1
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()
    
    glBegin(GL_LINES)
    for edge in edges:
        glColor3fv(colors[1])
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

pygame.init()
display = (1000,800)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
pygame.display.set_caption("MENTORSHIP")
clock = pygame.time.Clock()

gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0, 0, -15)

glEnable(GL_DEPTH_TEST)

p = Peripheral("24:71:89:09:90:84")
services = p.getServiceByUUID("F000AA80-0451-4000-B000-000000000000")

characs = services.getCharacteristics()
print(characs)
actCharacs = bytes.fromhex("7F00")
actCharacs2 = bytes.fromhex("0A")
print(actCharacs)

characs[1].write(actCharacs)
characs[2].write(actCharacs2)

Xaold = 0
Yaold = 0

def sensorLogic():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                glTranslatef(-0.5,0,0)
            if event.key == pygame.K_LEFT:
                glTranslatef(0.5,0,0)

    global characs
    
    h = characs[0].read().hex()
    h = str(h)
    Xgh = h[12:16]
    Ygh = h[16:20]
    Zgh = h[20:24]
    Zgyroh = h[8:12]
    Xi = hexToSignedInt(Xgh)
    Yi = hexToSignedInt(Ygh)
    Zi = hexToSignedInt(Zgh)
    Zgyroi = hexToSignedInt(Zgyroh)
    
##    # v magnetic field in microteslas
##    Xmagi = hexToSignedInt(Xmagh)
##    Ymagi = hexToSignedInt(Ymagh)
##    Zmagi = hexToSignedInt(Zmagh)
    
    # v accleration values (in Gs) on each axis
    X = (Xi * 1.0) / (32768 / 8)
    Y = (Yi * 1.0) / (32768 / 8)
    Z = (Zi * 1.0) / (32768 / 8)
    
##    Za = (Zgyroi * 1.0) / (65536 / 500)
    
    if Z == 0:
        Z = 0.001
    Xa = numpy.degrees(numpy.arctan2(Y, Z))
    denominator = math.sqrt(math.pow(Y,2) + math.pow(Z,2))
    Ya = numpy.degrees(numpy.arctan2(-X, denominator))
                
##    znum = Zmagi * math.sin(Xa) - Ymagi * math.cos(Xa)
##    zden = (Xmagi * math.cos(Ya)) + (Ymagi * math.sin(Ya) * math.sin(Xa)) + (Zmagi * math.sin(Ya) * math.cos(Xa))
##    Za = numpy.degrees(numpy.arctan2(znum, zden))
    
    global Xaold
    global Yaold
    glRotatef(Xa - Xaold, 1, 0, 0)
    glRotatef(-(Ya - Yaold), 0, 0, 1)                
    Xaold = Xa
    Yaold = Ya

    print("X",X)
    print("Y",Y)
    print("Z",Z)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    Cube()
    pygame.display.flip()
    clock.tick(60)

sensorLogic()
