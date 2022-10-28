import unittest

from server import NetProtocol


class TestNetwork(unittest.TestCase):
    def test_make_msg(self):
        net = NetProtocol()
        data = "https://ru.wikipedia.org/wiki/Python"

        msg = net.make_msg(data, False)
        self.assertEqual(msg, "0https://ru.wikipedia.org/wiki/Python\n".encode())

        msg = net.make_msg(data, True)
        self.assertEqual(msg, "1https://ru.wikipedia.org/wiki/Python\n".encode())

        msg = net.make_msg("abc")
        self.assertEqual(msg, "0abc\n".encode())

        msg = net.make_msg("")
        self.assertEqual(msg, "0\n".encode())

    def test_read_msg(self):
        net = NetProtocol()

        msg = "0https://ru.wikipedia.org/wiki/Python\n".encode()
        data = net.read_msg(msg)
        self.assertEqual(data, [(False, "https://ru.wikipedia.org/wiki/Python")])

        msg = "1https://ru.wikipedia.org/wiki/Python\n".encode()
        data = net.read_msg(msg)
        self.assertEqual(data, [(True, "https://ru.wikipedia.org/wiki/Python")])

        msg = "0\n".encode()
        data = net.read_msg(msg)
        self.assertEqual(data, [(False, "")])

        msg = "0abc\n1qwerty\n".encode()
        data = net.read_msg(msg)
        self.assertEqual(data, [(False, "abc"), (True, "qwerty")])

        msg = "0abc\n1qwerty\n0inbuff".encode()
        data = net.read_msg(msg)
        self.assertEqual(data, [(False, "abc"), (True, "qwerty")])
        self.assertEqual(net.buffer, "0inbuff")

        msg = "abc\n".encode()
        data = net.read_msg(msg)
        self.assertEqual(data, [(False, "inbuffabc")])
