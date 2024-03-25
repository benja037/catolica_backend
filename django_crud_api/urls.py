from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/',include('tasks.urls')),
    re_path('register', views.register),
    re_path('profile', views.profile),
    path('api/', include('tasks.api.urls')),
  
]

urlpatterns += static(settings.MEDIA_URL, documen_root=settings.MEDIA_ROOT)