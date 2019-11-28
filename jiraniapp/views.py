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
@login_required(login_url='/accounts/login/')
def home_projects (request):
    # Display all projects here:

    if request.GET.get('search_term'):
        businesses = Business.search_businesses(request.GET.get('search_term'))

    else:
        businesses = Business.objects.all()

    if request.GET.get('search_term'):
        neighbourhoods = Neighbourhood.search_neighbourhood(request.GET.get('search_term'))

    else:
        neighbourhoods = Neighbourhood.objects.all()


    if request.GET.get('search_term'):
        projects = Project.search_project(request.GET.get('search_term'))

    else:
        projects = Project.objects.all()

    form = NewsLetterForm

    if request.method == 'POST':
        form = NewsLetterForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name=name, email=email)
            recipient.save()
            send_welcome_email(name, email)

            HttpResponseRedirect('home_projects')


    return render(request, 'index.html', {'projects':projects, 'letterForm':form,
                                          'businesses':businesses,
                                          'neighbourhoods':neighbourhoods})

def business(request, id):

    try:
        business = Business.objects.get(pk = id)

    except DoesNotExist:
        raise Http404()

    return render(request, 'business.html', {"business": business})      

def neighbourhood(request, id):

    try:
        neighbourhood = Neighbourhood.objects.get(pk = id)
        business = Business.objects.filter(neighbourhood_id=neighbourhood)

    except DoesNotExist:
        raise Http404()

    return render(request, 'neighbourhood.html', {"neighbourhood": neighbourhood, 'business':business})

def project(request, id):

    try:
        project = Project.objects.get(pk = id)

    except DoesNotExist:
        raise Http404()

    current_user = request.user
    comments = Review.get_comment(Review, id)
    latest_review_list=Review.objects.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():

            comment = form.cleaned_data['comment']
            review = Review()
            review.project = project
            review.user = current_user
            review.comment = comment

            review.save()

    else:
        form = ReviewForm()

        # return HttpResponseRedirect(reverse('image', args=(image.id,)))

    return render(request, 'image.html', {"project": project,
                                          'form':form,
                                          'comments':comments,
                                          'latest_review_list':latest_review_list})
