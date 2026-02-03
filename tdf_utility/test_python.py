# asynchronous version
import asyncio
import time

async def serve_sandwitch():
    print("Preparing your sandwich...")
    await asyncio.sleep(5)
    print("Your sandwich is ready!")

async def serve_coffee():
    print("Brewing your coffee...")
    await asyncio.sleep(3)
    print("Your coffee is ready!")

async def runner():
    start_time = time.time()

    # batch = asyncio.gather(serve_sandwitch(), serve_coffee())
    # create_sandwitch, create_coffee = await batch

    task1 = asyncio.create_task(serve_sandwitch())
    task2 = asyncio.create_task(serve_coffee())
    await task1
    await task2

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    asyncio.run(runner())