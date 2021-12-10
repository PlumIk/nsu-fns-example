import os
from unittest import TestCase
from dotenv import load_dotenv
from for_flask.worker import Worker


class TestEnvVar(TestCase):
    def test_env_var_ok(self):
        load_dotenv()
        url = Worker.back_url()
        self.assertEqual('http://blablabla:8080/hmc/api/v1/fns/qr-code-response', url)

    def test_env_var_no_var(self):
        with self.assertRaises(ValueError) as exc:
            Worker.back_url()
        self.assertEquals(str(exc.exception), 'Variable "URL_TO_BACK" is not set')
