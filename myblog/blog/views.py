from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, IntegerField, Sum
import json
from django.urls import reverse
from blog.forms import *
from .models import *

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

def adminregistration(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']

                )
            u = UserRole(user=user, role_id = 1)
            u.save()
            return render(request, 'success.html',
                {
                 'admin': 1
                })
    else:
        form = RegisterForm()
        return render(request, 'adminregister.html', {
             'form': form
         })

@login_required(login_url="/blog/login/")
def dashboard(request):

    user_role = UserRole.objects.filter(user_id = request.user.id)
    role_id = user_role[0].role_id
    post = Post.objects.annotate(Count('comment')).order_by('updated_at')
    return render(request,"dashboard.html",
        {
		 'post': post,
         'role_id': role_id,
         'user_id': request.user.id
		})

def home(request):

        comments = Comment.objects.all().order_by('post_id')
        return render(request,"home.html",
            {
             'comments': comments
            
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

            return HttpResponseRedirect(reverse('blog:dashboard'))
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

def deleteuser(request):
    User.objects.filter()

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
        return HttpResponseRedirect(reverse('blog:dashboard'))
    else:
        posts = Post.objects.get(id=post_id)
        posts_cat = PostCategory.objects.get(post_id = post_id)
        posts_tag_id = PostTag.objects.filter(post_id = post_id)
        
        tags = ''
        for pt in posts_tag_id:
            tags += pt.tag.name + ', '
            
        data = {'title': posts.title, 'content': posts.content, 'tags': tags}
        form = CreatePostForm(initial=data)
        return render(request, 'editpost.html', {
             'form': form,
             'category': cat,
             'category_id': posts_cat.category.id,
             'post_id': post_id
         })

def deletepost(request, post_id):

    Post.objects.filter(id=post_id).delete()
    return HttpResponseRedirect(reverse('blog:dashboard'))

def viewpost(request, post_id):

    post_tag = PostTag.objects.filter(post_id = post_id)
    post_cat = PostCategory.objects.filter(post_id = post_id)
    comments = Comment.objects.filter(post_id = post_id)
    if request.user.id:
        user_role = UserRole.objects.filter(user_id = request.user.id)
        role_id = user_role[0].role_id
    else:
        role_id = 0
    viewers = post_cat[0].post.viewers
    viewers += 1
    Post.objects.filter(id = post_id).update(
                viewers = viewers
                )
    tag_name = ''
    for pt in post_tag:
        tag_name += pt.tag.name.title() + ', '
        
    tag_name = tag_name[:-2]
    for pc in post_cat:
        category_name = pc.category.name.title()
        post_title = pc.post.title.title()
        post_content = pc.post.content
        user_name = pc.post.user.username.title()

    comment_form = CommentForm()
    c = UserComment.objects.values('comment').\
        annotate(like_sum=Sum('like_count'))
    post_cmnt = UserComment.objects.filter(post_id = post_id, user_id=request.user.id)
    return render(request, 'viewpost.html', {
             'category_name': category_name,
             'post_title': post_title,
             'post_content': post_content,
             'user_name': user_name,
             'tag_name': tag_name,
             'CommentForm': CommentForm,
             'post_id': post_id,
             'comments': comments,
             'role_id': role_id,
             'user_id': request.user.id,
             'post_user_id': post_cat[0].post.user.id,
             'likecnt': c,
             'post_cmnt': post_cmnt
         })

def savecomment(request, post_id):
    user_id =request.user.id
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            comment1 = Comment.objects.create(
                comment_text = comment,
                post = Post(id = post_id),
                user = User(id = user_id),
                created_at = timezone.now()
                )
            UserComment.objects.create(
                user = User(id = user_id),
                comment = comment1,
                post = Post(id = post_id)

                )
        return HttpResponseRedirect(reverse('blog:viewpost', args=[post_id]))

def manage_like(request):

    if request.is_ajax():
        cmnt_id = request.GET.get('cmnt_id', '')
        like_cnt = request.GET.get('like_cnt', '')
        post_id = request.GET.get('post_id', '')
        like_cnt = int(like_cnt)
        like_unlike_val = request.GET.get('like_unlike_val', '')
        like_unlike_val = int(like_unlike_val)
        comments = UserComment.objects.filter(comment_id= cmnt_id, user_id =request.user.id)
        print comments.query
        if not comments:
            UserComment.objects.create(
                user = User(id = request.user.id),
                comment = Comment(id = cmnt_id),
                like_count = like_cnt,
                like_unlike = like_unlike_val,
                post_id = post_id
                )
        else:
            UserComment.objects.filter(id = comments[0].id).update(
                like_count = like_cnt,
                like_unlike = like_unlike_val
                )
            
        data = json.dumps('success')
    else:
        data = json.dumps('fail')
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def delete_comment(request):

    if request.is_ajax():
       cat_id = request.GET.get('cat_id', '')
       Comment.objects.filter(id = cat_id ).delete()
       data = ''
       mimetype = 'application/json'
       return HttpResponse(data, mimetype)
