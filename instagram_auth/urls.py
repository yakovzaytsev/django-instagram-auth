from django.conf.urls import url
from instagram_auth import views

urlpatterns = [
    url(r'^oauth_callback/', views.login_instagram, name='login_instagram'),
    url(r'^logout$', views.logout, name='logout'),
]

