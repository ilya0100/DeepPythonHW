# pylint: disable=protected-access

from asyncio import create_task
import aiounittest

from unittest.mock import AsyncMock, patch
from aiounittest.mock import AsyncMockIterator
from faker import Faker
from fetcher import Fetcher


class TestFetcher(aiounittest.AsyncTestCase):
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
        page_text = [fake.text() for _ in range(5)]
        mock_iter = AsyncMockIterator(page_text)

        fetcher = Fetcher()

        for url in urls:
            await fetcher._queue.put(url)

        session_mock = AsyncMock()
        resp_mock = AsyncMock()
        session_mock.get.return_value.__aenter__.return_value = resp_mock
        resp_mock.text.return_value = mock_iter

        async with session_mock.get(url) as resp:
            page = await resp.text()
            print(page)

        task = create_task(fetcher._fetch_url(session_mock))
        await task
        task.cancel()

        self.assertTrue(fetcher._queue.empty())
        for expected_text in page_text:
            text = await fetcher._out_queue.get()
            self.assertEqual(expected_text, text)
