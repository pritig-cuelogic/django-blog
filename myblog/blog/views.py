from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from blog.forms import *
from .models import UserRole, Post

@csrf_protect
def register(request):
	
    if request.method == 'POST':
    	form = RegisterForm(request.POST)
    	if form.is_valid():
    		user = User.objects.create_user(
    			username=form.cleaned_data['username'],
    			password=form.cleaned_data['password1'],
    			email=form.cleaned_data['email']

    			)
    		u = UserRole(user=user)
    		u.save()
    		return render(request, 'success.html')
    	else:
    		return render(request, 'register.html',
    			{
    			   'form': form
    			})
        
    else:
    	form = RegisterForm()
    	return render(request, 'register.html', {
		     'form': form
		 })

@login_required(login_url="login/")
def home(request):
	print request.user.id
	post = Post.objects.filter(user_id = request.user.id)
	return render(request,"home.html",
		{
		 'post': post
		})

def createpost(request):

	if request.method == 'POST':
		form = CreatePostForm(request.POST)
		if form.is_valid():
			post = Post.objects.create(
    			title = form.cleaned_data['title'],
    			content = form.cleaned_data['content'],
    			created_at = timezone.now(),
    			updated_at = timezone.now(),
    			user_id = request.user.id

    			)
			return HttpResponseRedirect(reverse('blog:home'))

	else:
		form = CreatePostForm()
		print Category.objects.all().order_by('id')
		print form
    	return render(request, 'createpost.html', {
		     'form': form
		 })
