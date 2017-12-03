from django.conf.urls import include, url
from instagram_auth import urls as instagram_auth_urls

urlpatterns = [
    url(r'^accounts/', include(instagram_auth_urls)),
]
