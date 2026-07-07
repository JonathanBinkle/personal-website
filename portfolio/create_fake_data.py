###############################################################################
# This script is used to create test database entries for development.
# It also creates a test superuser.
# Note: use "python manage.py flush --no-input" to delete any data.
###############################################################################

import os, django, sys, string
from django.conf import settings

# This is required to allow running the script directly from the CLI
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings")
django.setup()

# Always check that we're in DEBUG mode
if not settings.DEBUG:
    sys.exit("Don't create test data if you're not in DEBUG mode!")

# Create some fake data (use "faker" library if this isn't sufficient)
from blog.models import *
from django.contrib.auth.models import User
from random import shuffle, randint, choices
import datetime


def gen_random_word(min_length=3, max_length=8):
    word_length = randint(min_length, max_length)
    return "".join(choices(string.ascii_lowercase + "\n", k=word_length))


def gen_random_sentence(min_words=5, max_words=10):
    num_words = randint(min_words, max_words)
    return " ".join(gen_random_word() for _ in range(num_words))


def gen_random_paragraph(num_sentences=50):
    return ". ".join(gen_random_sentence() for _ in range(num_sentences)) + "."


def create_posts(num=5):
    min_n_sentences, max_n_sentences = 10, 500
    step_size = (max_n_sentences - min_n_sentences) / (num - 1) if num else 0
    num_sentences = [round(10 + i * step_size) for i in range(num)]

    for i in range(num):
        Posts.objects.create(
            title=f"My test title {i}",
            teaser=gen_random_sentence(),
            content=gen_random_paragraph(num_sentences[i]),
            datetime_published=datetime.datetime.now(tz=datetime.timezone.utc),
            is_draft=False,
        )


def create_tags(num=5):
    for i in range(num):
        Tags.objects.create(name=f"My tag {i}")


def assign_tags_to_some_posts():
    tags = list(Tags.objects.all())
    shuffle(tags)

    if len(tags) > 0:
        posts = list(Posts.objects.all())
        shuffle(posts)

        for post in posts[: randint(1, len(posts) - 1)]:
            for tag in tags[: randint(0, len(tags) - 1)]:
                post.tags.add(tag)


def create_superuser():
    admin, created = User.objects.get_or_create(
        username="TestAdmin",
        defaults={
            "first_name": "My",
            "last_name": "Admin",
            "email": "my.admin@example.com",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    admin.set_password("TestPassword")
    admin.save()


if __name__ == "__main__":
    print("\tCreating fake superuser ...")
    create_superuser()
    print("\tCreating fake posts ...")
    create_posts()
    print("\tCreating fake tags ...")
    create_tags()
    print("\tAssigning tags to posts ...")
    assign_tags_to_some_posts()
