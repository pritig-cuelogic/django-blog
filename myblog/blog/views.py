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
            tag_names = form.cleaned_data['tags']
            tag_names = tag_names[:-1]
            tag_name_list = tag_names.split(', ')
            tags = Tags.objects.all().order_by('id')
            tag_id_arr = []
            for tags_n in tag_name_list:
                for tag_obj in tags:
                    if tags_n == tag_obj.name:
                        tag_id_arr.append(tag_obj.id)
                        break
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
            for tag_id in tag_id_arr:
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

    cat =  Category.objects.all().order_by('id')
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            cat_id = request.POST.get('category', '')
            tag_names = form.cleaned_data['tags']
            tag_names = tag_names[:-1]
            tag_name_list = tag_names.split(', ')
            tags = Tags.objects.all().order_by('id')
            tag_id_arr = []
            for tags_n in tag_name_list:
                for tag_obj in tags:
                    if tags_n == tag_obj.name:
                        tag_id_arr.append(tag_obj.id)
                        break
            Post.objects.filter(id=post_id).update(
               title=form.cleaned_data['title'],
               content = form.cleaned_data['content'],
               updated_at = timezone.now()
            )
            PostCategory.objects.filter(post_id = post_id).update(
                category = Category(id = cat_id)
                )
            PostTag.objects.filter(post_id = post_id).delete()
            for tag_id in tag_id_arr:
                if tag_id:
                    PostTag.objects.create(
                        post = Post(id=post_id),
                        tag = Tags(id = tag_id)
                    )
        return HttpResponseRedirect(reverse('blog:home'))
    else:
        posts = Post.objects.get(id=post_id)
        posts_cat = PostCategory.objects.get(post_id = post_id)
        posts_tag_id = PostTag.objects.filter(post_id = post_id)
        
        tags = ''
        for pt in posts_tag_id:
            print pt.tag.id
            print pt.tag.name
            tags += pt.tag.name + ', '
            
        data = {'title': posts.title, 'content': posts.content, 'tags': tags}
        form = CreatePostForm(initial=data)
        return render(request, 'editpost.html', {
             'form': form,
             'category': cat,
             'category_id': posts_cat.category.id,
             'post_id': post_id
         })
    
