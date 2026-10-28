from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse


class LogoutMigrationTests(TestCase):
    def test_logout_uses_post_and_clears_session(self):
        user = get_user_model().objects.create_user(username='logout-test', password='test-password')
        self.client.force_login(user)

        page = self.client.get(reverse('homepage'))
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, 'method="post"')
        self.assertContains(page, "action='/logout/'")
        self.assertContains(page, 'name="csrfmiddlewaretoken"')
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)

        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, '/', fetch_redirect_response=False)
        self.assertNotIn(SESSION_KEY, self.client.session)
