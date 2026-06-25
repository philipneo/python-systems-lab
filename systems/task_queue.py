from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from time import perf_counter
from typing import Any

Job = Callable[[], Awaitable[Any]]


@dataclass
class QueueMetrics:
    completed: int = 0
    failed: int = 0
    retries: int = 0
    total_seconds: float = 0.0


class AsyncTaskQueue:
    def __init__(self, workers: int = 2, retries: int = 1) -> None:
        self.workers = workers
        self.retries = retries
        self.metrics = QueueMetrics()
        self._queue: asyncio.Queue[Job] = asyncio.Queue()

    async def submit(self, job: Job) -> None:
        await self._queue.put(job)

    async def run(self) -> QueueMetrics:
        workers = [asyncio.create_task(self._worker()) for _ in range(self.workers)]
        await self._queue.join()
        for worker in workers:
            worker.cancel()
        await asyncio.gather(*workers, return_exceptions=True)
        return self.metrics

    async def _worker(self) -> None:
        while True:
            job = await self._queue.get()
            start = perf_counter()
            try:
                await self._run_with_retries(job)
                self.metrics.completed += 1
            except Exception:
                self.metrics.failed += 1
            finally:
                self.metrics.total_seconds += perf_counter() - start
                self._queue.task_done()

    async def _run_with_retries(self, job: Job) -> None:
        for attempt in range(self.retries + 1):
            try:
                await job()
                return
            except Exception:
                if attempt == self.retries:
                    raise
                self.metrics.retries += 1
                await asyncio.sleep(0.05 * (attempt + 1))
