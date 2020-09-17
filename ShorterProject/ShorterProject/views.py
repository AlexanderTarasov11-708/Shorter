from django.http import Http404
from django.shortcuts import render, redirect
from django.db.models import F
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from ShorterProject import models


def home(request):
    url_error = False
    url_input = ""
    shortened_url = ""

    if request.method == "POST":
        validator = URLValidator()
        try:
            url_input = request.POST.get("url", None)
            if not url_input:
                url_error = True
            else:
                validator(url_input)
        except ValidationError:
            url_error = True

        if not url_error:
            link_db = models.Link()
            link_db.link = url_input
            link_db.hash = link_db.get_hash()
            link_db.save()
            shortened_url = request.build_absolute_uri(link_db.hash)
            url_input = ""

    return render(request, "index.html",
                  {"error": url_error, "url": url_input, "shorturl": shortened_url})


def redir(request, link_hash):
    try:
        link = models.Link.objects.get(hash=link_hash)
        models.Link.objects.filter(hash=link_hash).update(hits=F('hits') + 1)
        return redirect(link.link)
    except ObjectDoesNotExist:
        raise Http404()


def all(request):
    all_results = models.Link.objects.all().order_by('-hits')
    return render(request, "links.html",
                  {"all_results": all_results, "all": "active"})
