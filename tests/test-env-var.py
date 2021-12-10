import os
from unittest import TestCase
from dotenv import load_dotenv


class TestEnvVar(TestCase):
    def test_env_var(self):
        load_dotenv()
        url = f'{os.getenv("URL_TO_BACK")}hmc/api/v1/fns/qr-code-response'
        self.assertEqual('http://blablabla:8080/hmc/api/v1/fns/qr-code-response', url)
