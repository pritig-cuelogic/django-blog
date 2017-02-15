from django.conf.urls import url
from django.contrib.auth import views as auth_views
from blog.forms import LoginForm

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'register/$', views.register, name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 
        'authentication_form': LoginForm},name = 'login'),
    url(r'home/$', views.home, name='home'),
    url(r'createpost/$', views.createpost, name='createpost'),
    url(r'editpost/(?P<post_id>\d+)$', views.editpost, name='editpost'),
    url(r'get_tags/$', views.get_tags, name='get_tags'),
]
