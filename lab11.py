# Intermediate programming practice: async and sockets.
#
# For EACH problem, work out your problem-solving OUTLINE first, then implement it (you
# may use an AI assistant to help - see the README). The async parts must actually run
# their work CONCURRENTLY (that's the whole point), not one after another.
#
# Do not rename the functions - the tests use these names.

import asyncio
import socket


async def gather_doubled(numbers):
    # Outline:
    #   1. If `numbers` is empty, return [].
    #   2. Define a small async helper coroutine that takes `n` and returns `n * 2`.
    #   3. Create a coroutine object for each item in `numbers` and pass them all
    #      unpacking-style (`*coros`) into `asyncio.gather(...)` so they run concurrently.
    #   4. Convert/return the gathered results as a `list` preserving the original order.

    async def double(n):
        return n * 2

    results = await asyncio.gather(*(double(n) for n in numbers))
    return list(results)


async def fastest(jobs):
    # Outline:
    #   1. If `jobs` is empty, return None.
    #   2. Define an async worker coroutine for each `(label, delay)` pair that awaits
    #      `asyncio.sleep(delay)` and returns `label`.
    #   3. Schedule/start all coroutines concurrently and iterate over them as they
    #      finish using `asyncio.as_completed(...)`.
    #   4. Await the very first completed coroutine and return its `label`.

    if not jobs:
        return None

    async def run_job(label, delay):
        await asyncio.sleep(delay)
        return label

    coros = [run_job(label, delay) for label, delay in jobs]
    for finished_coro in asyncio.as_completed(coros):
        return await finished_coro


def echo_once(host, port, message):
    # Outline:
    #   1. Create a TCP socket (`AF_INET`, `SOCK_STREAM`) using a `with` context manager
    #      so it closes automatically.
    #   2. Connect to `(host, port)`.
    #   3. Encode `message` to UTF-8 bytes and send everything via `.sendall(...)`.
    #   4. Receive bytes back from the server with `.recv(1024)` and decode back to `str`.
    #   5. Return the decoded string.

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(message.encode())
        reply = sock.recv(1024)
    return reply.decode()


def main():
    print(asyncio.run(gather_doubled([1, 2, 3, 4])))  # [2, 4, 6, 8]
    print(asyncio.run(fastest([("A", 0.06), ("B", 0.02), ("C", 0.04)])))  # B


if __name__ == "__main__":
    main()
