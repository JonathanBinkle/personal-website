from django.contrib.syndication.views import Feed
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from .models import Posts, Tags


def _filter_posts_by_tags(request, tag_ids):
    """
    List all posts that match at least one of the specified tags.
    If no tags are given, show all posts.
    """
    if request.method == "POST" and (query := request.POST.get("search_field")):
        # Post matches if (case insensitive) query in title/teaser/content
        matches = Posts.objects.filter(
            Q(title__icontains=query)
            | Q(teaser__icontains=query)
            | Q(content__icontains=query)
            #| Q(datetime_published__date__icontains=query)
            #| Q(datetime_last_modified__date__icontains=query)
        )
        return render(
            request,
            "blog/posts_overview.html",
            {
                "posts": matches or None,
                "only_draft_posts": matches.filter(is_draft=False).count() == 0,
                "no_search_matches": matches.count() == 0,
            },
        )

    matches = set()

    for tag_id in tag_ids:
        if tag := Tags.objects.filter(id=tag_id).first():
            matches.update(set(p for p in tag.posts_set.all()))

    matches = sorted(matches, key=lambda post: post.datetime_published, reverse=True)

    if not tag_ids:
        matches = Posts.objects.all()

    return render(
        request,
        "blog/posts_overview.html",
        {
            "posts": matches or None,
            "only_draft_posts": sum([int(p.is_draft) for p in matches]) == len(matches),
            "invalid_tag": tag_ids and not matches,
        },
    )


def index(request):
    """
    Redirect to the posts_overview.
    """
    return redirect(to="blog:posts_overview")


def posts_overview(request):
    """
    List all posts or all posts matching the search query.
    """
    return _filter_posts_by_tags(request, [])


def posts_filtered_by_tag(request, id):
    """
    List all posts with the specified tag.
    """
    return _filter_posts_by_tags(request, [id])


def tags_overview(request):
    """
    List tags, sorted descending by popularity.
    Draft-only and unused tags are only visible to admins.
    """
    is_admin = request.user.is_superuser

    tags = []
    for tag in Tags.objects.all():
        n_total = tag.posts_set.all().count()
        n_draft = tag.posts_set.filter(is_draft=True).count()
        draft_only = n_total == n_draft

        if not draft_only or (draft_only and is_admin):
            tag_details = {
                "id": tag.id,
                "name": tag.name,
                "count": n_total if is_admin else n_total - n_draft,
                "draft_only": draft_only,
            }

            tags.append(tag_details)

    tags.sort(key=lambda tag: tag["count"], reverse=True)

    return render(request, "blog/tags_overview.html", {"tags": tags or None})


def post(request, id):
    """
    Show post details and links to next and previous posts.
    If the next/previous post is a draft and the user isn't an admin, find the
    next/previous non-draft post or show "no such post".
    """
    context = {}

    if post := Posts.objects.filter(id=id).first():
        if request.user.is_superuser:
            prev_post = Posts.objects.filter(
                datetime_published__lt=post.datetime_published
            ).first()
            next_post = Posts.objects.filter(
                datetime_published__gt=post.datetime_published
            ).last()
        else:
            prev_post = Posts.objects.filter(
                datetime_published__lt=post.datetime_published, is_draft=False
            ).first()
            next_post = Posts.objects.filter(
                datetime_published__gt=post.datetime_published, is_draft=False
            ).last()

        context.update({"prev_post": prev_post})
        context.update({"post": post})
        context.update({"next_post": next_post})

    return render(request, "blog/post.html", context)


class RssFeed(Feed):
    """
    See docs: https://docs.djangoproject.com/en/4.2/ref/contrib/syndication/
    """

    title = "Jonathan Binkle's blog"
    link = "/blog/rss/"
    description = "All blog posts."

    def items(self):
        return Posts.objects.filter(is_draft=False)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.teaser

    def item_link(self, item):
        return reverse("blog:post", args=[item.pk])
