from django.shortcuts import render, redirect
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.core.files.storage import FileSystemStorage
import os


def home(request):
    return render(request, "core/home.html", {})


def contact(request):
    return render(request, "core/contact.html", {})


def privacy_policy(request):
    return render(request, "core/privacy_policy.html", {})


def view_file(request, file: str):
    """
    Redirects to file viewer if the file exists, else returns 404.
    The `file` format is '<name>.<extension>' e.g. 'test.pdf'.
    """
    file = os.path.basename(file)  # prevent path traversal
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    if not fs.exists(str(file)):
        raise Http404

    return redirect(fs.url(file))
