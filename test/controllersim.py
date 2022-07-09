
import asyncio
from socket import SocketIO
import zmq
import zmq.asyncio
import pickle


context = zmq.asyncio.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")



async def main () :
    while True:
        message =await socket.recv()
        print(message)
        if message == b"slac" :
            socket.send(b"1")
            print("YES")

        else :
            socket.send(b"0")
            print("NO")



asyncio.run(main())





