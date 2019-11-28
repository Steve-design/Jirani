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

@login_required(login_url='/accounts/login/')
def new_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('homePage')

    else:
        form = NewImageForm()
    return render(request, 'registration/new_image.html', {"form": form})

@login_required(login_url='/accounts/login/')
def new_business(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewBusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user
            business.save()
        return redirect('homePage')

    else:
        form = NewBusinessForm()
    return render(request, 'registration/new_business.html', {"form": form})


@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()
        return redirect('homePage')

    else:
        form = NewProjectForm()
    return render(request, 'registration/new_project.html', {"form": form})

@login_required(login_url='/accounts/login/')
def new_neighbourhood(request):
    current_user = request.user
    if request.method == 'POST':
        form = CreateNeighbourhoodForm(request.POST, request.FILES)
        if form.is_valid():
            neighbourhood = form.save(commit=False)
            neighbourhood.user = current_user
            neighbourhood.save()
        return redirect('homePage')

    else:
        form = CreateNeighbourhoodForm()
    return render(request, 'registration/new_neighbourhood.html', {"form": form})


@login_required(login_url='/accounts/login/')
def join(request, id):
    '''
    This view function will implement adding
    '''
    neighbourhood = Neighbourhood.objects.get(pk=id)
    if Join.objects.filter(user_id=request.user).exists():

        Join.objects.filter(user_id=request.user).update(neighbourhood_id=neighbourhood)

        return redirect(reverse('neighbourhood', args=(neighbourhood.id,)))

    else:

        Join(user_id=request.user, neighbourhood_id=neighbourhood).save()

    print("success")
    return redirect('homePage')  

@login_required(login_url='/accounts/login/')
def exit(request, id):

    neighbourhood = Neighbourhood.objects.get(pk=id)
    if Join.objects.filter(user_id=request.user).exists():

        Join.objects.filter(user_id=request.user).delete()

        return redirect(reverse('neighbourhood', args=(neighbourhood.id,)))

    else:

        Join(user_id=request.user, neighbourhood_id=neighbourhood).delete()

    print("success")
    return redirect('homePage')      
