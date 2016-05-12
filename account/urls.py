from django.conf.urls import url

from . import views

app_name = 'account'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^dash/$', views.dash, name='dash'),
    # Might be a better way to go about this one but just to test this is probably the best way....
    url(r'^create_new_invite_key/$', views.create_new_invite_key, name='Create new Invite Key'),

]
