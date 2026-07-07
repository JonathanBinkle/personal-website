from django.test import Client, TestCase
from django.db import IntegrityError, transaction
import datetime
from .models import Tags, Posts


class Tests(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.client = Client()
        super().__init__(methodName)

    def _create_post(self):
        return Posts.objects.create(
            title="My test title",
            teaser="My test teaser",
            content="My test content",
            datetime_published=datetime.datetime.now(tz=datetime.timezone.utc),
        )

    def _create_tag(self):
        return Tags.objects.create(name="My tag")

    def test_url_response(self):
        response = self.client.get("/blog/")
        self.assertRedirects(response, "/blog/posts/", target_status_code=200)

        for url in ["/blog/tags/", "/blog/posts/42/", "/blog/tags/42/", "/blog/rss/"]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_no_posts_warning(self):
        response = self.client.get("/blog/posts/")
        self.assertContains(response, "Sorry, but there are no posts yet...")

        self._create_post()
        response = self.client.get("/blog/posts/")
        self.assertNotContains(response, "Sorry, but there are no posts yet...")

    def test_no_such_post_warning(self):
        response = self.client.get("/blog/posts/42/")
        self.assertContains(response, "Sorry, but there is no such post...")

    def test_no_tags_warning(self):
        response = self.client.get("/blog/tags/")
        self.assertContains(response, "Sorry, but there are no tags yet...")

        tag = self._create_tag()
        post = self._create_post()
        post.tags.add(tag)
        response = self.client.get("/blog/tags/")
        self.assertNotContains(response, "Sorry, but there are no tags yet...")

    def test_no_such_tag_warning(self):
        response = self.client.get("/blog/tags/42/")
        self.assertContains(response, "Sorry, but there are no matching posts...")

    def test_post_is_shown(self):
        post = self._create_post()
        response = self.client.get("/blog/posts/")
        self.assertContains(response, post.title)
        self.assertContains(response, post.teaser)
        self.assertNotContains(response, post.content)
        # TODO: haven't yet figured out correct format to check DateTimeFields

    def test_tag_is_shown_only_when_referenced(self):
        tag = self._create_tag()
        response = self.client.get("/blog/tags/")
        self.assertNotContains(response, tag.name)

        post = self._create_post()
        post.tags.add(tag)
        response = self.client.get("/blog/tags/")
        self.assertContains(response, tag.name)

    def test_posts_must_have_unique_title(self):
        # https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.Field.unique
        with transaction.atomic():
            # https://stackoverflow.com/questions/21458387
            self._create_post()

        with self.assertRaises(IntegrityError):
            self._create_post()

    def test_tags_must_have_unique_name(self):
        with transaction.atomic():
            self._create_tag()

        with self.assertRaises(IntegrityError):
            self._create_tag()

    def test_show_all_posts_if_empty_search_query(self):
        post = self._create_post()
        response = self.client.post("/blog/posts/", {"search_field": ""})
        self.assertContains(response, post.title)
        self.assertContains(response, post.teaser)
        self.assertNotContains(response, post.content)

    def test_no_matching_post_in_search_warning(self):
        self._create_post()
        response = self.client.post("/blog/posts/", {"search_field": "blabla"})
        self.assertContains(response, "Sorry, but there are no matching posts...")
