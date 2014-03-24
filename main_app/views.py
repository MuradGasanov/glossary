# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect


def index(request):
    return render_to_response("index.html")