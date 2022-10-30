import socket

from queue import Queue
from argparse import ArgumentParser
from threading import Thread
from server import NetProtocol


class Client:
    def __init__(self, path, address="localhost", port=8080, threads_count=1, queue_size=10):
        self.path = path
        self.address = address
        self.port = port

        self._net = NetProtocol()

        self.threads_count = threads_count
        self._thread_list = None
        
        self._urls_pool = Queue(queue_size)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self._socket.connect((self.address, self.port))
        self._start_threads()

        self._parse_file()
        self.stop()

    def stop(self):
        for th in self._thread_list:
            th.join()
        self._socket.close()

    def _start_threads(self):
        self._thread_list = [
            Thread(target=self._make_request) for _ in range(self.threads_count)
        ]
        for th in self._thread_list:
            th.start()

    def _parse_file(self):
        with open(self.path, "r") as urls:
            for line in urls:
                if line.strip() == '':
                    continue

                url = line.strip()
                self._urls_pool.put((url, True))


        for _ in range(self.threads_count):
            self._urls_pool.put((None, None))

    def _make_request(self):
        while True:
            url, keep_alive = self._urls_pool.get()
            if url is None:
                break

            msg = self._net.make_msg(url, keep_alive)
            self._socket.sendall(msg)
            resp = self._socket.recv(1024)
            messages = self._net.read_msg(resp)

            for msg in messages:
                print(msg[1])


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", help="File with urls")
    parser.add_argument("-t", default=1, help="Therads count")

    args = parser.parse_args()

    client = Client(args.f, threads_count=int(args.t))
    client.start()
    client.stop()