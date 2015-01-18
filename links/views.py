from urlparse import urlparse
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from .models import Link, LinkForm

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
        request.session['short_url'] = "http://" + str(request.get_host()) + "/" + str(link.id)
        return redirect('/')
    raise Http404("Link does not exist")

def home(request):
  context = {'form': LinkForm}
  if 'short_url' in request.session:
    context['short_url'] = request.session['short_url']
  if 'url' in request.POST:
    link = Link(url=request.POST['url'])
    link.save();
    request.session['short_url'] = "http://" + request.get_host() + "/" + link.id
    return redirect('/')
  return render(request, 'index.html', context)