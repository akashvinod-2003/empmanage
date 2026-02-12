from django.contrib import admin
from django.urls import path, include
from ems import views as ems_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/logout/', ems_views.PostOnlyLogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', ems_views.home, name='home'),
    path('', include('ems.urls')),
]
