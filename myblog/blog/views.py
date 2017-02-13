from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from django.urls import reverse
from blog.forms import *
from .models import UserRole, Post, Category, Tags, PostCategory, PostTag

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
	post = Post.objects.filter(user_id = request.user.id)
	return render(request,"home.html",
		{
		 'post': post
		})

def createpost(request):

    cat =  Category.objects.all().order_by('id')
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            cat_id = request.POST.get('category', '')
            tag = (cat_id,request.POST.get('hidden_tag', ''))
            print "cat = %r and tag = %r and form = %r" % (cat_id,request.POST.get('hidden_tag', ''), form.cleaned_data)
            tag_list = set(tag[1].split(','))
            post = Post.objects.create(
                title = form.cleaned_data['title'],
                content = form.cleaned_data['content'],
                created_at = timezone.now(),
                updated_at = timezone.now(),
                user_id = request.user.id
                )
            PostCategory.objects.create(
                post = post,
                category = Category(id = cat_id)

                )
            for tag_id in tag_list:
                PostTag.objects.create(
                    post = post,
                    tag = Tags(id = tag_id)
                    )

            return HttpResponseRedirect(reverse('blog:home'))
        else:
            return render(request, 'createpost.html', {
             'form': form,
             'category': cat
         })

    else:
        form = CreatePostForm()
        return render(request, 'createpost.html', {
             'form': form,
             'category': cat
         })


def get_tags(request):

    if request.is_ajax():
        q = request.GET.get('term', '')
        tags = Tags.objects.filter(name__icontains = q )
        results = []
        for tag in tags:
            tag_json = {}
            tag_json['id'] = tag.id
            tag_json['label'] = tag.name
            tag_json['value'] = tag.name
            results.append(tag_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def editpost(request, post_id):
    return HttpResponse("hiii")
