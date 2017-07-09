#!/usr/bin/env python3

'''
roboclient_Keyboardinputs.py

Uses a keyboard input to send <X,Y,A> tuples to the create2server
over a socket.
'I' to move forward
'K' to move backward
'J' to turn left
'L' to turn right
'U' to make a forward left diagoanl curve
'O' to make a forward right diagonal curve
'M' to make a backward left diagonal curve
'.' to make a backward right diagonal curve
'A' to make a slow stop
'S' to decelerate
'D' to accelerate
X,Y are control axis (-1..+1); A is autopilot flag (0 or 1).


The MIT License

Copyright (c) 2016 Simon D. Levy
Copyright (c) 2017 Sarang Gujar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import socket
import pygame

#This is altered from roboclient, which takes keyboard inputs and send it to the create2server


# These should agree with the values in the server script!
host   = '10.88.7.223'
port    = 24900


# Index of autopilot button
AUTOPILOT_BUTTON = 0

# Connect to the server over a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((host, port)) # Note tuple!

except socket.error as error:
    print('connect() to ' + host + ':' + str(port) + ' failed: ' + str(error))

print('Connected to ' + host + ':' + str(port))

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((400, 300))

# Start with autopilot off
autopilot = False

# Index of base axis and velocity of controller
axis_x = 0
axis_y = 0
vel = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                print('key i')
                axis_x = 0
                axis_y = 1
                autopilot = True
                msg = '%+2.2f %+2.2f %d*' % (vel*axis_x, vel*axis_y, autopilot)
                print('msg = ', msg)
                # Send the message over the socket
                sock.send(msg.encode())
            elif event.key == pygame.K_k:
                print('key k')
                axis_x = 0
                axis_y = -1
                autopilot = True
                msg = '%+2.2f %+2.2f %d*' % (vel*axis_x, vel*axis_y, autopilot)
                print('msg = ', msg)
                # Send the message over the socket
                sock.send(msg.encode())
            elif event.key == pygame.K_j:
                print('key j')
                axis_x = -1
                axis_y = 0
                autopilot = True
                msg = '%+2.2f %+2.2f %d*' % (vel*axis_x, vel*axis_y, autopilot)
                print('msg = ', msg)
                # Send the message over the socket
                sock.send(msg.encode())
            elif event.key == pygame.K_l:
                print('key l')
                axis_x = 1
                axis_y = 0
                autopilot = True
                msg = '%+2.2f %+2.2f %d*' % (vel*axis_x, vel*axis_y, autopilot)
                print('msg = ', msg)
                # Send the message over the socket
                sock.send(msg.encode())
            elif event.key == pygame.K_a:
                print('K a = stop')
                vel = 0
                autopilot = True
                msg = '%+2.2f %+2.2f %d*' % (vel*axis_x, vel*axis_y, autopilot)
                print('msg = ', msg)
                # Send the message over the socket
                sock.send(msg.encode())
            elif event.key == pygame.K_s:
                print('K s')
                vel -= 0.1
                if (vel < 0):
                    vel = 0
                autopilot = True
                msg = '%+2.2f %+2.2f %d*' % (vel*axis_x, vel*axis_y, autopilot)
                print('msg = ', msg)
                # Send the message over the socket
                sock.send(msg.encode())
            elif event.key == pygame.K_d:
                print('K d')
                vel += 0.1
                if(vel > 1):
                    vel = 1
                autopilot = True
                msg = '%+2.2f %+2.2f %d*' % (vel*axis_x, vel*axis_y, autopilot)
                print('msg = ', msg)
                # Send the message over the socket
                sock.send(msg.encode())
            elif event.key == pygame.K_u:
                print('key u')
                axis_x = 1
                axis_y = 1
                autopilot = True
                msg = '%+2.2f %+2.2f %d*' % (vel*axis_x, vel*axis_y, autopilot)
                print('msg = ', msg)
                # Send the message over the socket
                sock.send(msg.encode())
            elif event.key == pygame.K_o:
                print('key j')
                axis_x = -1
                axis_y = 1
                autopilot = True
                msg = '%+2.2f %+2.2f %d*' % (vel*axis_x, vel*axis_y, autopilot)
                print('msg = ', msg)
                # Send the message over the socket
                sock.send(msg.encode())
            elif event.key == pygame.K_m:
                print('key l')
                axis_x = 1
                axis_y = -1
                autopilot = True
                msg = '%+2.2f %+2.2f %d*' % (vel*axis_x, vel*axis_y, autopilot)
                print('msg = ', msg)
                # Send the message over the socket
                sock.send(msg.encode())
            elif event.key == pygame.K_PERIOD:
                print('key PERIOD')
                axis_x = -1
                axis_y = -1
                autopilot = True
                msg = '%+2.2f %+2.2f %d*' % (vel*axis_x, vel*axis_y, autopilot)
                print('msg = ', msg)
                # Send the message over the socket
                sock.send(msg.encode())
