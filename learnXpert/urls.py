from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path("users/", include('apps.users.urls', namespace='users')),
    path("", include('apps.courses.urls', namespace='courses')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
