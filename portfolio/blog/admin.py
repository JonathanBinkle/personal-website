from django.contrib import admin
from .models import Tags, Posts, Images
import textwrap


class PostsAdmin(admin.ModelAdmin):
    exclude = ["reading_time"]

    # Extend the default admin template to show some hints
    # https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#overriding-admin-templates
    change_form_template = "blog/admin/change_form_posts.html"

    def render_change_form(self, request, context, *args, **kwargs):
        context["snippets"] = {
            "Link to image:": textwrap.dedent("""
            <figure>
            <img src="/media/blog_images/IMAGE_NAME.EXT" alt="DESCRIPTION" width="100%">
            <figcaption>CAPTION</figcaption>
            </figure>
            """),
            "Link to file:": textwrap.dedent("""
            <a
                class="btn btn-sm btn-warning" 
                role="button" 
                href="/files/FILE_NAME.EXT"
                target="_blank">
                    DESCRIPTION
            </a>
            """),
            "Table of contents:": textwrap.dedent("""
            ---

            <strong>Contents</strong>:

            [TOC]

            ---
            <br>
            """),
        }
        return super().render_change_form(request, context, *args, **kwargs)


admin.site.register(Posts, PostsAdmin)
admin.site.register(Tags)
admin.site.register(Images)
