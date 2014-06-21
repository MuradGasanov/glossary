# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from main_app import models
from datetime import *
from dateutil import tz
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


def login_error(request):
    return render_to_response("login.html", {"error": "Вы не можете быть авторизованны,"
                                                      " доступ разрешен только для домена apertura.su"})


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")


def index(request):
    return render_to_response("index.html", {"is_authenticated": request.user.is_authenticated()})


def get_titles(request):
    project = request.POST.get("project")
    titles = models.Term.objects.extra(
        select={"t": "UPPER(LEFT(title,1))"})
    if project:
        titles = titles.filter(project_id=int(project))
    titles = list(titles.values_list("t", flat=True).distinct().order_by("t"))
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
        project = options.get("project", 0)
        sort_by_name = options.get("sort_by_name", True)

        if sort_by_name:
            terms = terms.order_by("title")
        else:
            terms = terms.order_by("-create_at")

        if query:
            if start_width:
                terms = terms.filter(title__istartswith=query)
            else:
                terms = terms.filter(title__icontains=query)

        if project:
            terms = terms.filter(project_id=int(project))

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
            "project": term.project.name if term.project else "",
            "project_id": term.project.id if term.project else "",
            "create_at": str(term.create_at),
            "can_edit": (term.author.id == request.user.id) or request.user.is_staff
        })

    return HttpResponse(json.dumps({"items": items, "total": total}), content_type="application/json")


@login_required(redirect_field_name=None)
def create_term(request):
    item = json.loads(request.POST.get("item"))

    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    project = item.get("project", 0)
    if type(project) == unicode and len(project) != 0:
        project = models.Project.objects.create(name=project, author=request.user)
    elif type(project) == int and project != 0:
        project = models.Project.objects.get(id=project)
    else:
        project = None

    new_term = models.Term.objects.create(
        title=item.get("title"),
        description=item.get("description"),
        project=project,
        create_at=datetime.now(),
        author=request.user
    )

    return HttpResponse(json.dumps({
        "id": new_term.id,
        "title": new_term.title,
        "description": new_term.description,
        "author": new_term.author.username,
        "author_id": new_term.author.id,
        "project": new_term.project.name if new_term.project else "",
        "project_id": new_term.project.id if new_term.project else "",
        "create_at": str(new_term.create_at),
        "can_edit": True
    }), content_type="application/json")


@login_required(redirect_field_name=None)
def update_term(request):
    item = json.loads(request.POST.get("item"))
    term = models.Term.objects.get(id=item.get("id"))

    if term.author.id != request.user.id:
        if not request.user.is_staff:
            return HttpResponseForbidden()

    project = item.get("project", 0)
    if type(project) == unicode and len(project) != 0:
        project = models.Project.objects.create(name=project, author=request.user)
    elif type(project) == int and project != 0:
        project = models.Project.objects.get(id=project)
    else:
        project = None

    term.title = item.get("title")
    term.description = item.get("description")
    term.project = project
    term.create_at = datetime.now()

    term.save()

    return HttpResponse(json.dumps({
        "id": term.id,
        "title": term.title,
        "description": term.description,
        "author": term.author.username,
        "author_id": term.author.id,
        "project": term.project.name if term.project else "",
        "project_id": term.project.id if term.project else "",
        "create_at": str(term.create_at),
        "can_edit": True
    }), content_type="application/json")


@login_required(redirect_field_name=None)
def remove_term(request):
    item = json.loads(request.POST.get("item"))
    term = models.Term.objects.get(id=item.get("id"))

    if term.author.id != request.user.id:
        if not request.user.is_staff:
            return HttpResponseForbidden()

    term.delete()

    return HttpResponse("ok", content_type="application/json")


def get_projects(request):
    projects = list(models.Project.objects.all().order_by("name").values("id", "name"))

    if projects:
        return HttpResponse(json.dumps(projects), content_type="application/json")
    else:
        return HttpResponse("[]", content_type="application/json")


def search_suggestions(request):
    project = request.POST.get("project", 0)
    titles = models.Term.objects.all()

    if project:
        titles = titles.filter(project=int(project))

    titles = list(titles.values_list("title", flat=True))

    return HttpResponse(json.dumps(titles), content_type="application/json")