from urllib.parse import urlparse
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.db.models import F
from django.contrib import messages
from .models import Link, LinkForm


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def catchall(request, id):
    try:
        link = Link.objects.get(id=id)
        parsed = urlparse(link.url)
        Link.objects.filter(id=id).update(clicks=F("clicks") + 1)
        if parsed.scheme:
            return redirect(link.url)
        return redirect("https://" + link.url)
    except Exception as e:
        return HttpResponse(e)
        parsed = urlparse(id)
        if parsed.netloc:
            link = Link(url=id, ip=get_client_ip(request))
            link.save()
            request.session["short_url"] = (
                "https://" + str(request.get_host()) + "/" + str(link.id)
            )
            return redirect("/")
    raise Http404("Link does not exist")


def home(request):
    context = {"form": LinkForm}
    if "short_url" in request.session and request.session["short_url"]:
        context["short_url"] = request.session["short_url"]
        request.session["short_url"] = None
    if "url" in request.POST:
        link = Link(url=request.POST["url"], ip=get_client_ip(request))
        link.save()
        request.session["short_url"] = "https://" + request.get_host() + "/" + link.id
        return redirect("/")
    return render(request, "index.html", context)
