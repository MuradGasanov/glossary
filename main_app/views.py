# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from main_app import models
import json


def index(request):
    titles = models.Term.objects.extra(
        select={"t": "UPPER(LEFT(title,1))"}
    ).values_list("t", flat=True).distinct().order_by("t")
    return render_to_response("index.html", {"titles": titles})


def get_terms(request):
    options = None
    if "options" in request.POST:
        options = json.loads(request.POST.get("options"))

    terms = models.Term.objects.all()
    total = terms.count()

    if options:
        skip = options.get("skip", None)
        take = options.get("take", None)
        query = options.get("query", "")
        start_width = options.get("start_width", False)

        if query:
            if start_width:
                terms = terms.filter(title__istartswith=query)
            else:
                terms = terms.filter(title__icontains=query)

        total = terms.count()
        terms = terms[skip:skip + take]

    items = list(terms.values("title", "description"))

    return HttpResponse(json.dumps({"items": items, "total": total}), content_type="application/json")


def search_suggestions(request):
    titles = list(models.Term.objects.all().values_list("title", flat=True))
    return HttpResponse(json.dumps(titles), content_type="application/json")