from pathlib import Path
import asyncio
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from systems.task_queue import AsyncTaskQueue


async def make_job(name: str, delay: float):
    async def job() -> None:
        await asyncio.sleep(delay)
        print(f"completed {name}")
    return job


async def main() -> None:
    queue = AsyncTaskQueue(workers=3, retries=2)

    for index in range(8):
        await queue.submit(await make_job(f"job-{index}", 0.05))

    metrics = await queue.run()
    print(metrics)


if __name__ == "__main__":
    asyncio.run(main())
