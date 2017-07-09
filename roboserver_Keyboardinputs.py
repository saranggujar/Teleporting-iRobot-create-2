#!/usr/bin/env python3

'''
robotserver_Keyboardinputs.py

Serves a socket that accepts <X,Y,A> tuples from a client's keyboard.

X,Y are control axes (-1..+1); A is autopilot flag (0 or 1).

This code is part of BreezyCreate2

The MIT License

Copyright (c) 2016 Simon D. Levy, Rajwol Joshi, Jamie White, Logan Wilson
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

from breezycreate2 import Robot
from time import sleep
import socket
import threading

# These values should be changed according to availavle network 
HOST   = '10.88.7.223'
PORT    = 24900
BUFSIZE = 100


def threadfunc(values, vel, rvel):

    # Connect to the Create2
    bot = Robot()
    
    while True:
    
        s = 0.75
        print( values[0],' ', values[1], 'vel = ', vel , 'rvel = ', rvel )
        vel = s * vel + (1-s) * values[1]
        rvel = s * rvel + (1-s) * values[0]
        if( values[0] == 0 and values[1] == 0 and abs(vel) < 0.1 ):
            bot.setTurnSpeed(0)
        elif( values[0] == 0 ):
            bot.setForwardSpeed(500*vel)
            print('Forward only ', vel )
        elif( values[1] == 0 ):
            bot.setTurnSpeed(500*rvel)
            print('Turn only ', rvel)
        else:
            bot.setCustomSpeed(500*vel, 500*rvel)
            print('Custom Speed ', 500*vel,' ',500*rvel)
        sleep(0.1)
        
if __name__ == '__main__':

    # Listen for a client ------------------------------------------------------
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.bind((HOST, PORT)) # Note tuple!

    except socket.error as error:
       print('bind() failed on ' + HOST + ':' + str(PORT) + ' ' + str(error))
       exit(1)

    print('Waiting for a client ...')

    sock.listen(1)  # handle up to 1 back-logged connection

    client, address = sock.accept()

    print('Accepted connection')

    # These values will be shared with the command-listener thread
    values = [0,0,0]
    vel = 0
    rvel = 0

    # Launch command listener on another thread
    thread = threading.Thread(target=threadfunc, args = (values,vel,rvel,))
    thread.daemon = True
    thread.start()

    # Loop forever, getting <X,Y,A> tuples from the client and sharing them with
    # the command listener
    while True:

        msg = ''

        messages = client.recv(BUFSIZE).decode().split('*')
        for message in messages:
            parts = message.split()
            if len(parts) == 3:
                values[0] = float(parts[0])
                values[1] = float(parts[1])
                values[2] = int(parts[2])
