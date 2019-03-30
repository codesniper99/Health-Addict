from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from core.decorators import check_recaptcha

from . import views


urlpatterns = [   
    path('dev/admin/', admin.site.urls),
    re_path(r'^$', views.index, name='home'),
    # path('login/', check_recaptcha(auth_views.LoginView.as_view()), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    re_path(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
    re_path(r'^notifications/', include('notify.urls', 'notifications')),
    re_path(r'^reset-password/$', PasswordResetView.as_view(), name='reset_password'),
    re_path(r'^reset-password/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset-password/confirm/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^reset-password/complete/$', PasswordResetCompleteView.as_view(), name='password_reset_complete')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    import debug_toolbar
    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls)),]