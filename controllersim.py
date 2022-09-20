from enum import IntEnum
import asyncio
from socket import SocketIO
from sre_parse import State
from typing import Dict
import zmq
import zmq.asyncio
import pickle

from cp_handler import CPStates


context = zmq.asyncio.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")



async def zmq_send ( state :str , message , protocol :str = "controller") :

        dumped_msg = pickle.dumps (
            {
             "state" : state , 
             "message" : message ,
             "protocol" : protocol,
            }
        )
        await socket.send(dumped_msg)


async def main () :
    while True:
        message =await socket.recv()
        dump :dict = pickle.loads(message)
        try :
            value = dump.get("message")
            print(value)
            if value == "init" :
                await zmq_send("init",message="YES")
            elif value == "cp_write" :
                print("SENDINGGG")
                await zmq_send("init",message=pickle.dumps(CPStates.A))
        except KeyError :
            print(value)
        
        # if message == b"slac" :
        #     socket.send(b"1")
        #     print("YES")

        # if dump.get("state") == "slac" :
        #     print("YESSSSSS")

        

        



asyncio.run(main())





