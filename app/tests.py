from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import ID_LENGTH, Link, generate_unique_id


class GenerateUniqueIdTests(TestCase):
    def test_returns_correct_length(self):
        id = generate_unique_id()
        self.assertEqual(len(id), ID_LENGTH)

    def test_returns_different_id_on_collision(self):
        Link.objects.create(id="aaaaaaaa", url="https://example.com")
        with patch("app.models.secrets.token_urlsafe", side_effect=["aaaaaaaa", "bbbbbbbb"]):
            id = generate_unique_id()
        self.assertEqual(id, "bbbbbbbb")

    def test_raises_after_max_attempts(self):
        with patch("app.models.secrets.token_urlsafe", return_value="aaaaaaaa"):
            Link.objects.create(id="aaaaaaaa", url="https://example.com")
            with self.assertRaises(RuntimeError):
                generate_unique_id()


class LinkModelTests(TestCase):
    def test_save_generates_id(self):
        link = Link(url="https://example.com")
        link.save()
        self.assertIsNotNone(link.id)
        self.assertEqual(len(link.id), ID_LENGTH)

    def test_save_does_not_overwrite_existing_id(self):
        link = Link.objects.create(id="myid123", url="https://example.com")
        link.url = "https://other.com"
        link.save()
        self.assertEqual(link.id, "myid123")

    def test_str(self):
        link = Link(url="https://example.com")
        self.assertEqual(str(link), "https://example.com")


class HomeViewTests(TestCase):
    def test_get_renders_form(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_post_creates_link_and_redirects(self):
        response = self.client.post(reverse("home"), {"url": "https://example.com"})
        self.assertRedirects(response, "/")
        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(Link.objects.first().url, "https://example.com")

    def test_post_sets_short_url_in_session(self):
        self.client.post(reverse("home"), {"url": "https://example.com"})
        self.assertIn("short_url", self.client.session)
        self.assertIn(Link.objects.first().id, self.client.session["short_url"])

    def test_short_url_shown_and_cleared_from_session(self):
        self.client.post(reverse("home"), {"url": "https://example.com"})
        # First GET after POST should show the short_url
        response = self.client.get(reverse("home"))
        self.assertIn("short_url", response.context)
        # Second GET should no longer have it
        response = self.client.get(reverse("home"))
        self.assertNotIn("short_url", response.context)

    def test_post_records_client_ip(self):
        self.client.post(
            reverse("home"),
            {"url": "https://example.com"},
            REMOTE_ADDR="1.2.3.4",
        )
        self.assertEqual(Link.objects.first().ip, "1.2.3.4")

    def test_post_prefers_x_forwarded_for(self):
        self.client.post(
            reverse("home"),
            {"url": "https://example.com"},
            HTTP_X_FORWARDED_FOR="5.6.7.8, 1.2.3.4",
        )
        self.assertEqual(Link.objects.first().ip, "5.6.7.8")


class RedirectLinkViewTests(TestCase):
    def setUp(self):
        self.link = Link.objects.create(id="abcd1234", url="https://example.com")

    def test_redirects_to_url(self):
        response = self.client.get(reverse("short", args=["abcd1234"]))
        self.assertRedirects(response, "https://example.com", fetch_redirect_response=False)

    def test_increments_click_count(self):
        self.client.get(reverse("short", args=["abcd1234"]))
        self.link.refresh_from_db()
        self.assertEqual(self.link.clicks, 1)

    def test_prepends_https_when_no_scheme(self):
        Link.objects.create(id="noscheme", url="example.com")
        response = self.client.get(reverse("short", args=["noscheme"]))
        self.assertRedirects(response, "https://example.com", fetch_redirect_response=False)

    def test_returns_404_for_unknown_id(self):
        response = self.client.get(reverse("short", args=["notfound"]))
        self.assertEqual(response.status_code, 404)


class ShortenFromPathViewTests(TestCase):
    def test_creates_link_and_redirects_home(self):
        response = self.client.get("/https://example.com")
        self.assertRedirects(response, "/")
        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(Link.objects.first().url, "https://example.com")

    def test_sets_short_url_in_session(self):
        self.client.get("/https://example.com")
        self.assertIn("short_url", self.client.session)

    def test_returns_404_for_plain_string(self):
        response = self.client.get(reverse("short", args=["notaurl"]))
        self.assertEqual(response.status_code, 404)


class LinkFormTests(TestCase):
    def test_valid_url(self):
        from .forms import LinkForm
        form = LinkForm(data={"url": "https://example.com"})
        self.assertTrue(form.is_valid())

    def test_invalid_url(self):
        from .forms import LinkForm
        form = LinkForm(data={"url": "not a url"})
        self.assertFalse(form.is_valid())

    def test_empty_url(self):
        from .forms import LinkForm
        form = LinkForm(data={"url": ""})
        self.assertFalse(form.is_valid())
