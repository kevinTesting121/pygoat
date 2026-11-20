from django.contrib.auth import get_user_model
from django.test import TestCase


class SqlLabInjectionTests(TestCase):
    def setUp(self):
        self.account = get_user_model().objects.create_user(username="victim", password="secret")
        self.client.force_login(self.account)

    def test_sql_injection_cannot_read_account_passwords(self):
        response = self.client.post("/injection_sql_lab", {
            "name": "x' UNION SELECT group_concat(password),'x' FROM auth_user-- ",
            "pass": "x",
        })

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.account.password)
        self.assertNotContains(response, "Logged in as:")

    def test_demo_credentials_still_work(self):
        response = self.client.post("/injection_sql_lab", {"name": "jack", "pass": "jack"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user1"], "jack")
