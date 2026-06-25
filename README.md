# Python Systems Lab

Advanced Python systems practice with caching, task queues, concurrency, and lightweight observability.

## Focus Areas

- LRU cache design
- Async task execution
- Retry behavior
- Structured metrics
- Testable systems components

## Included Modules

- `systems/cache.py` - LRU cache using `OrderedDict`
- `systems/task_queue.py` - asyncio worker queue with retries
- `examples/run_queue.py` - runnable async queue demo

## Run Example

```bash
python examples/run_queue.py
```

## Why This Exists

This repo is for practicing backend-style thinking: state, failure, concurrency, and clear interfaces.
