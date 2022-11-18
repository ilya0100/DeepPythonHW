from pprint import PrettyPrinter
import re

from argparse import ArgumentParser
from asyncio import Queue, create_task, run
from collections import Counter
from time import time
from bs4 import BeautifulSoup
from aiohttp import ClientSession


class Fetcher:
    def __init__(self, workers_count=10, words_count=3):
        self._words_count = words_count
        self._workers_count = workers_count

        self._workers = []

        self._queue = Queue()
        self._out_queue = Queue()

    def parse_url(self, page):
        bsoup = BeautifulSoup(page, features="html.parser")
        words = re.findall(r"\w+", bsoup.get_text().lower())
        most_common = dict(Counter(words).most_common(self._words_count))
        return most_common

    async def _fetch_url(self, session):
        while True:
            url = await self._queue.get()

            try:
                async with session.get(url) as resp:
                    page = await resp.text()
                    print(page)
                    await self._out_queue.put(self.parse_url(page))
            finally:
                self._queue.task_done()

    async def fetch(self, urls):
        for url in urls:
            await self._queue.put(url)

        async with ClientSession() as session:
            self._workers = [
                create_task(self._fetch_url(session)) for _ in range(self._workers_count)
            ]

            await self._queue.join()
        
        output = []
        while not self._out_queue.empty():
            result = await self._out_queue.get()
            output.append(result)
            self._out_queue.task_done()
        return output
    
    def cancel(self):
        for worker in self._workers:
            worker.cancel()


async def main():
    parser = ArgumentParser()
    parser.add_argument("-c", default=10, help="Workers count")
    parser.add_argument("-f", default=10, help="File path")

    fetcher_args = parser.parse_args()
    fetcher = Fetcher(int(fetcher_args.c))

    urls = []
    with open(fetcher_args.f, "r", encoding="utf-8") as urls_file:
        for url in urls_file:
            urls.append(url)

    time_1 = time()
    result = await fetcher.fetch(urls)
    time_2 = time()

    fetcher.cancel()
    printer = PrettyPrinter()
    printer.pprint(result)
    print(f"{len(result)=}")
    print("Time:", time_2 - time_1)

if __name__ == "__main__":
    run(main())