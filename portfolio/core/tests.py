from django.test import Client, TestCase
from django.conf import settings


class Tests(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.client = Client()
        super().__init__(methodName)

    def test_url_response(self):
        for url in ["/", "/contact/", "/privacy-policy/"]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
