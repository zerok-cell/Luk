import asyncio


async def x():
    await asyncio.sleep(5)
    print('1231231232')


async def y():
    print('1232')


async def main():
    asyncio.create_task(x())
    asyncio.create_task(y())


asyncio.run(main())
