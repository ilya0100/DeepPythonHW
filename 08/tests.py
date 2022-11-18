# pylint: disable=protected-access

from asyncio import create_task
from unittest.mock import AsyncMock, Mock, patch
from unittest.async_case import IsolatedAsyncioTestCase

from faker import Faker
from fetcher import Fetcher


class TestFetcher(IsolatedAsyncioTestCase):
    def test_parse_url(self):
        test_cases = [
            {
                "text": "word, ..'word'', qwerty %(QWERTY something!@ +)WORD&(@%",  # noqa
                "expected_result": {"word": 3, "qwerty": 2, "something": 1},
            },
            {"text": "", "expected_result": {}},
            {
                "text": "word qwerty something",
                "expected_result": {"word": 1, "qwerty": 1, "something": 1},
            },
        ]

        with patch("fetcher.BeautifulSoup") as bs_mock:
            bs_instance = bs_mock.return_value
            for case in test_cases:
                bs_instance.get_text.return_value = case["text"]

                fetcher = Fetcher(1, 4)
                result = fetcher.parse_url("")

                self.assertEqual(case["expected_result"], result)

    async def test_fetch_url(self):
        fake = Faker()
        urls = [fake.url() for _ in range(5)]
        page_text = fake.text()

        fetcher = Fetcher()

        for url in urls:
            await fetcher._queue.put(url)

        session_mock = Mock()
        resp_mock = AsyncMock()
        session_mock.get.return_value = resp_mock
        resp_mock.__aenter__.return_value.text.return_value = page_text

        task = create_task(fetcher._fetch_url(session_mock))
        await fetcher._queue.join()
        task.cancel()

        self.assertTrue(fetcher._queue.empty())
        expected_result = fetcher.parse_url(page_text)
        while not fetcher._out_queue.empty():
            text = await fetcher._out_queue.get()
            self.assertEqual(expected_result, text)

    async def test_fetch(self):
        fake = Faker()
        urls = [fake.url() for _ in range(10)]

        fetcher = Fetcher(workers_count=5)

        async def side_effect(_):
            while True:
                url = await fetcher._queue.get()
                await fetcher._out_queue.put(url)
                fetcher._queue.task_done()

        with patch("fetcher.Fetcher._fetch_url") as fetch_url_mock:
            fetch_url_mock.side_effect = side_effect
            result = await fetcher.fetch(urls)

        for worker in fetcher._workers:
            self.assertFalse(worker.done())

        self.assertTrue(fetcher._queue.empty())
        self.assertTrue(fetcher._out_queue.empty())
        self.assertListEqual(urls, result)

        fetcher.cancel()
