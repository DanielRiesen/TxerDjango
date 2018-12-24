from django.urls import path, include
from django.contrib import admin
from rest_framework.authtoken import views


urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('API/', include('Tutorials.urls')),
    path('admin/', admin.site.urls),
    path('API/', include('Txer.urls')),
]
