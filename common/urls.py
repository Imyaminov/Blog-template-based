from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='common/logout.html'), name='logout'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='common/password_reset.html',
         ),
         name='password_reset'
         ),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password_reset_done.html'
         ),
         name='password_reset_done'
         ),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password_reset_confirm.html',
         ),
         name='password_reset_confirm'
         ),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(
         template_name='common/password_reset_complete.html',
         ),
         name='password_reset_complete'
         )


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

