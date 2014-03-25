# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from main_app import models
import json


def index(request):
    return render_to_response("index.html")


def get_terms(request):
    options = None
    if "options" in request.POST:
        options = json.loads(request.POST.get("options"))

    total = models.Term.objects.all().count()

    if options:
        skip = options.get("skip", 0)
        take = options.get("take", 0)
        query = options.get("query", "")
        if query:
            terms = models.Term.objects.filter(title__icontains=query)
            total = terms.count()
        else:
            terms = models.Term.objects.all()[skip:skip + take]
    else:
        terms = models.Term.objects.all()

    items = list(terms.values("title", "description"))

    if items:
        return HttpResponse(json.dumps({"items": items, "total": total}), content_type="application/json")
    else:
        return HttpResponse(json.dumps(""), content_type="application/json")


def search_suggestions(request):
    titles = list(models.Term.objects.all().values_list("title", flat=True))
    return HttpResponse(json.dumps(titles), content_type="application/json")