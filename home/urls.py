from django.conf.urls import url

from . import views

# TODO Might Change this.... Might not!
app_name = 'home'
urlpatterns = [
    # Homepage
    url(r'^$', views.index, name='index'),
    # Details page
    url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
    # Add Comment
    url(r'^(?P<post_id>[0-9]+)/add_comment/$', views.addComment, name='add_comment'),
    # New Post
    url(r'^new_post/$', views.newPost, name='new_post'),
]
