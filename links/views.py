from django.shortcuts import render, redirect
from django.http import Http404
from .models import Link, LinkForm
from urlparse import urlparse

def catchall(request, id):
    try:
      link = Link.objects.get(id=id)
      return redirect(link.url)
    except:
      parsed = urlparse(id)
      if parsed.netloc:
        link = Link(url=id)
        link.save();
        context = {'form': LinkForm}
        context['short_url'] = "http://" + str(request.get_host()) + "/" + str(link.id)
        return render(request, 'index.html', context)
    raise Http404("Link does not exist")

def home(request):
  context = {'form': LinkForm}
  if 'url' in request.POST:
    link = Link(url=request.POST['url'])
    link.save();
    context['short_url'] = "http://" + str(request.get_host()) + "/" + str(link.id)
  return render(request, 'index.html', context)