from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()
	is_active =  models.BooleanField(default=1)

class Comment(models.Model):
	comment_text = models.TextField()
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField()

class Category(models.Model):
	name = models.CharField(max_length=50)

class PostCategory(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

class UserRole(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	role_id = models.IntegerField(default=2)

class Tags(models.Model):
	name = models.CharField(max_length=50)

class PostTag(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
