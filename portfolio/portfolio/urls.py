from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from os import getenv
from .sitemaps import PostSitemap, GenericSitemap

urlpatterns = [
    path("", include(("core.urls", "core"), namespace="core")),
    path("blog/", include(("blog.urls", "blog"), namespace="blog")),
    # Change "admin/" to something else to make automatic attacks a bit harder
    path(str(getenv("ADMIN_PATH")), admin.site.urls),
    # Sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"posts": PostSitemap, "generic": GenericSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
