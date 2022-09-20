import asyncio
from multiprocessing import cpu_count
from typing import Awaitable
from driver import (
    Adc,
    Pwm,
)
from utils import wait_for_tasks
from enum import IntEnum
import logging


class PwmState(IntEnum):
    EVSE_READY = 100
    EVSE_DIG_COMM = 5
    EVSE_NOT_READY = 0


class CPStates(IntEnum):
    NONE = 0
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("CP_Handler")


class CPHandler:

    def __init__(self, callback) -> None:

        self.cp_current_state: CPStates = CPStates.NONE

        self.cp_last_state: CPStates = CPStates.NONE

        self.callback = callback

        self.created_task: Awaitable
        # Creating The Pwm Driver Instance
        self.pwm = Pwm()
        # Creating The Adc Driver Instance
        self.adc = Adc()

        logger.info("Initializing <CP Handler> Module")

    async def start(self):

        # TODO First Here WE should Write The Cp state And Then Read it State
        await self.write_cp(PwmState.EVSE_READY)
        await asyncio.sleep(0.02)
        self.cp_current_state = await self.cp_state_calculator()
        self.cp_last_state = self.cp_current_state

    async def start_cp_routin(self):
        tasks = [self.loop_handling()]
        await wait_for_tasks(tasks)

    async def loop_handling(self):
        while True:

            self.cp_current_state = await self.cp_state_calculator()

            if self.cp_current_state != self.cp_last_state:
                # task = asyncio.create_task(self.callback(self.cp_current_state))
                await self.callback(self.cp_current_state)

            self.cp_last_state = self.cp_current_state
            await asyncio.sleep(0.001)

    async def read_cp(self) -> int:
        return self.adc.read_voltage()

    async def write_cp(self, state: PwmState):
        logger.info(f"Writing CP to : {state}")
        self.pwm.Pwm_SetDutyCycle(state)

    async def cp_state_calculator(self) -> "CPStates":
        state: CPStates = CPStates.NONE
        voltage: float = await self.read_cp()
        # print(voltage)
        if voltage >= 11:
            state = CPStates.A
        elif (voltage >= 8) and (voltage < 11):
            state = CPStates.B
        return state

    def get_task(self, task: Awaitable):
        self.created_task = task
