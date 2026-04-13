import logging
from urllib.parse import urlparse

from django.db.models import F
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import LinkForm
from .models import Link

logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def redirect_link(request, id):
    try:
        link = Link.objects.get(id=id)
    except Link.DoesNotExist:
        raise Http404("Link does not exist")
    Link.objects.filter(id=id).update(clicks=F("clicks") + 1)
    if urlparse(link.url).scheme:
        return redirect(link.url)
    return redirect("https://" + link.url)


def shorten_from_path(request, url):
    parsed = urlparse(url)
    if not parsed.netloc:
        raise Http404("Link does not exist")
    link = Link(url=url, ip=get_client_ip(request))
    link.save()
    request.session["short_url"] = (
        "https://" + str(request.get_host()) + "/" + str(link.id)
    )
    return redirect("/")


def catchall(request, id):
    if Link.objects.filter(id=id).exists():
        return redirect_link(request, id)
    return shorten_from_path(request, id)


def home(request):
    context = {"form": LinkForm}
    if "short_url" in request.session and request.session["short_url"]:
        context["short_url"] = request.session["short_url"]
        del request.session["short_url"]
    if "url" in request.POST:
        link = Link(url=request.POST["url"], ip=get_client_ip(request))
        link.save()
        request.session["short_url"] = "https://" + request.get_host() + "/" + link.id
        return redirect("/")
    return render(request, "index.html", context)
