import re
import json
import socket
import urllib.error

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from collections import Counter
from itertools import count
from queue import Queue
from threading import Lock, Thread, current_thread
from time import sleep
from urllib.request import urlopen


def parse_url(url, words_count):
    page = urlopen(url, timeout=1)
    bs = BeautifulSoup(page.read(), features="html.parser")

    words = re.findall(r"\w+", bs.get_text().lower())
    most_common = dict(Counter(words).most_common(words_count))
    return most_common


class NetProtocol:
    def __init__(self):
        self.buffer = ''
        
    def make_msg(self, data, keep_alive=False):
        keep_alive = int(keep_alive)
        result = f"{keep_alive}{data}\n"
        return result.encode()

    def read_msg(self, data):
        data = data.decode()

        messages = f"{self.buffer}{data}".split('\n')
        if messages[-1] != '':
            self.buffer = messages[-1]
        del messages[-1]

        for i, msg in enumerate(messages):
            messages[i] = (bool(int(msg[0])), msg[1:])

        return messages


class Server:
    def __init__(self, address="localhost", port=8080, workers_count=1, queue_size=10):
        self.address = address
        self.port = port
        self.workers_count = workers_count

        self._net = NetProtocol()

        self._tasks_processed = count()

        self._thread_list = None
        self._task_queue = Queue(queue_size)

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self, func, *args, backlog=0):
        print("Strarting server with args:", f"{func=}, {args=}, {backlog=}")
        self._socket.bind((self.address, self.port))
        self._socket.listen(backlog)

        self._start_workers(func, *args)

        while True:
            try:
                conn, _ = self._socket.accept()
                self._net.buffer = ""
                keep_alive = True
                while keep_alive:
                    req = conn.recv(1024)
                    if not req:
                        break
                    messages = self._net.read_msg(req)

                    keep_alive = messages[-1][0]

                    for msg in messages:
                        self._task_queue.put((*msg, conn))
            except KeyboardInterrupt:
                self.stop()
                break

    def stop(self):
        for _ in range(self.workers_count):
            self._task_queue.put(None)
        for th in self._thread_list:
            th.join()
        self._socket.close()

    def _start_workers(self, func, *args):
        print("Strarting", self.workers_count, "workers")
        self._thread_list = [
            Thread(target=self._worker_routine, args=(func, *args)) for _ in range(self.workers_count)
        ]
        for th in self._thread_list:
            th.start()

    def _worker_routine(self, func, *args):
        print("Strart routine at thread:", current_thread())
        while True:
            task = self._task_queue.get()
            if task is None:
                break
            keep_alive, data, conn = task

            try:
                resp = func(data, *args)
                resp = json.dumps(resp, ensure_ascii=False)
                resp = f"{data}: {resp}"
            except ValueError as err:
                resp = f"{data}: {err}"
            except urllib.error.HTTPError as err:
                resp = f"{data}: HTTP error: {err.code}"
            except urllib.error.URLError as err:
                resp = f"{data}: network error"
            finally:
                conn.sendall(self._net.make_msg(resp))
                self._task_queue.task_done()

            with Lock():
                print("Number of processed tasks:", next(self._tasks_processed) + 1)

            if keep_alive == False:
                while self._task_queue.unfinished_tasks > 0:
                    sleep(0.5)
                conn.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-w", default=1, help="Workers count")
    parser.add_argument("-k", default=5, help="Number of most common words")

    args = parser.parse_args()

    server = Server(workers_count=int(args.w))
    server.start(parse_url, int(args.k))
