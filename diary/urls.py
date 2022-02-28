from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.obtain_auth_token, name="obtain-auth-token"),
    path('api/', include('story.urls'), )
]