import asyncio
from multiprocessing import cpu_count
from typing import Awaitable
import aiofile
from utils import wait_for_tasks
from enum import IntEnum
import logging



class CPStates (IntEnum) :
    NONE = 0
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    

CP_READ_DIR = "/sys/class/leds/input3::capslock/brightness"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("CP_Handler")



class CPHandler () :
    
    def __init__(self , callback) -> None:
        
        self.cp_current_state : CPStates = CPStates.NONE 

        self.cp_last_state : CPStates = CPStates.NONE

        self.callback : Awaitable = callback

        self.created_task : Awaitable = None

        logger.info("Initilalizing <CP Handler> Module")

        

    async def start (self) :
        #TODO First Here WE should Write The Cp state And Then Read it State
        self.cp_current_state =  await self.cp_state_calculator()
        
        tasks = [self.loop_handling()]
        await wait_for_tasks(tasks)
        
        

    async def loop_handling (self) :
        while (True) :

            self.cp_current_state = await self.cp_state_calculator()
            
            if self.cp_current_state != self.cp_last_state :
                # task = asyncio.create_task(self.callback(self.cp_current_state))
                await self.callback(self.cp_current_state)
                

            self.cp_last_state = self.cp_current_state
            


    async def read_cp (self) -> int:
        async with aiofile.async_open(CP_READ_DIR) as file :
            adc_value = await file.read(1)
            return int(adc_value)

    async def write_cp (self,cp_state : CPStates) :
        logger.info(f"Writing CP to : {cp_state}")
        #TODO Need To write this on the SECC

    async def cp_state_calculator (self) -> "CPStates":
        state : CPStates = None
        adc_value:int = await self.read_cp()
        if adc_value == 0 :
            state = CPStates.A 
        elif adc_value == 1 :
            state = CPStates.B
        return state


    def get_task(self,task : Awaitable) :
        self.created_task = task
        






            
            






            

        