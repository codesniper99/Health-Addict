from django.shortcuts import render, redirect
from django.conf import settings


def index(request):
    return render(request=request, template_name='index.html')

