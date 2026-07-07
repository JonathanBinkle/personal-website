from django.contrib.sitemaps import Sitemap
from blog.models import Posts
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls import reverse

from django.urls import NoReverseMatch


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Posts.objects.filter(is_draft=False)

    def lastmod(self, obj):
        return obj.datetime_last_modified

    def location(self, obj):
        return reverse("blog:post", kwargs={"id": obj.id})


class GenericSitemap(Sitemap):
    """
    List endpoints specified in `urlpatterns` of all custom apps.
    Doesn't list endpoints that expect an attribute, such as files/<str:file>.
    """

    changefreq = "monthly"
    priority = 0.5

    def items(self):
        app_urlpatterns = []
        for app in settings.CUSTOM_APPS:
            app_urlpatterns += self.get_urlpatterns_for_app(app)

        return [url.name for url in app_urlpatterns if url.name is not None]

    def get_urlpatterns_for_app(self, app_name):
        app_urls = import_string(f"{app_name}.urls")

        # Exclude URLs that take an argument, e.g. "files/<str:file>"
        # TODO: in future fix this to return "files/" instead of excluding it
        return [url for url in app_urls.urlpatterns if not ":" in str(url.pattern)]

    def location(self, item):
        for app in settings.CUSTOM_APPS:
            app_urls = import_string(f"{app}.urls")
            for url in app_urls.urlpatterns:
                if url.name == item:
                    # NOTE: assumes namespace is app name
                    return reverse(f"{app}:{item}")
