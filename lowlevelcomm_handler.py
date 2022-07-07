from concurrent.futures import wait
from re import L
from cp_handler import (
    CPHandler,
    CPStates ,
)

from slac_session import (
    SlacEvseSession,
)

from zmq_handler import (
    CommunicationHandler,
)

from utils import(
    wait_for_tasks
)


class LowLevelCommHandler :
    def __init__(self) -> None:
        self.slac_handler = SlacEvseSession(iface="enp0s31f6" , evse_id="Pokileda")
        self.cp_handler = CPHandler(self.cp_event)
        self.comm_handler = CommunicationHandler()

        self.state = 0


    async def start (self) :
        list_of_tasks = [
            self.cp_handler.start()
        ]

        await wait_for_tasks(list_of_tasks)

    async def cp_event (self,cp_state : CPStates) :
        if self.cp_handler.cp_current_state == CPStates.B and self.state == 0 :
            await self.slac_handler.evse_start_slac_association()
            self.state = 1

        if self.cp_handler.cp_current_state == CPStates.B and self.state == 1 :
            await self.slac_handler.evse_stop_slac_association()
            self.state = 0




    


