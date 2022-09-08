from lowlevelcomm_handler import LowLevelCommHandler
import asyncio


async def main():
    handler = LowLevelCommHandler()
    await handler.start()

     
def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()

