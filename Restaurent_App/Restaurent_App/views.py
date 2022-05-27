from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    return HttpResponseRedirect(reverse('Product_App:index'))