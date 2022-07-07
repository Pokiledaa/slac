from lowlevelcomm_handler import LowLevelCommHandler
import asyncio




async def main() :
    handler = LowLevelCommHandler()
    await handler.start()
    

    
if __name__ == "__main__" :

    asyncio.run(main())

