# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from main_app import models
from datetime import *
import json


def log_in(request):

    if request.user.is_authenticated():
        HttpResponseRedirect("/")

    try:
        data = json.loads(request.body)
    except (TypeError, ValueError):
        return render_to_response("login.html")

    username = data.get("login", "")
    password = data.get("password", "")

    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
        request.session.set_expiry(timedelta(days=1).seconds)
        if user.is_active:
            return HttpResponse(json.dumps({"error": []}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"error": ["Пользователь заблокирован"]}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"error": ["Неверный логин и пароль"]}), content_type="application/json")


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")


def index(request):
    return render_to_response("index.html", {"is_authenticated": request.user.is_authenticated()})


def get_titles(request):
    titles = list(models.Term.objects.extra(
        select={"t": "UPPER(LEFT(title,1))"}
    ).values_list("t", flat=True).distinct().order_by("t"))
    return HttpResponse(json.dumps({"items": titles}), content_type="application/json")


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

    # items = list(terms.values("title", "description", "author__id", "author__name"))

    items = []

    for term in terms:
        items.append({
            "id": term.id,
            "title": term.title,
            "description": term.description,
            "author": term.author.username,
            "author_id": term.author.id,
            "can_edit": (term.author.id == request.user.id) or request.user.is_staff
        })

    return HttpResponse(json.dumps({"items": items, "total": total}), content_type="application/json")


def create_term(request):
    item = json.loads(request.POST.get("item"))

    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    new_term = models.Term.objects.create(
        title=item.get("title"),
        description=item.get("description"),
        author=request.user
    )

    return HttpResponse(json.dumps({
        "id": new_term.id,
        "title": new_term.title,
        "description": new_term.description,
        "author": new_term.author.username,
        "author_id": new_term.author.id,
        "can_edit": (new_term.author.id == request.user.id) or request.user.is_staff
    }), content_type="application/json")


def update_term(request):
    item = json.loads(request.POST.get("item"))
    term = models.Term.objects.get(id=item.get("id"))

    if (term.author.id != request.user.id) or request.user.is_staff:
        return HttpResponseForbidden()

    term.title = item.get("title")
    term.description = item.get("description")

    term.save()

    return HttpResponse(json.dumps({
        "id": term.id,
        "title": term.title,
        "description": term.description,
        "author": term.author.username,
        "author_id": term.author.id,
        "can_edit": (term.author.id == request.user.id) or request.user.is_staff
    }), content_type="application/json")


def remove_term(request):
    item = json.loads(request.POST.get("item"))
    term = models.Term.objects.get(id=item.get("id"))

    if (term.author.id != request.user.id) or request.user.is_staff:
        return HttpResponseForbidden()

    term.delete()

    return HttpResponse(json.dumps("ok"), content_type="application/json")


def search_suggestions(request):
    titles = list(models.Term.objects.all().values_list("title", flat=True))
    return HttpResponse(json.dumps(titles), content_type="application/json")