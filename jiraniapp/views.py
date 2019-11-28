from django.shortcuts import render, redirect, get_object_or_404
from __future__ import unicode_literals
from .models import *
from django.http  import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from .email import send_welcome_email
from django.urls import reverse

# Create your views here.
