from django.urls import path
from . import views
from .oauth import ion_login, ion_callback, ion_logout

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('oauth/login/', ion_login, name='ion_login'),
    path('oauth/callback/', ion_callback, name='ion_callback'),
    path('oauth/logout/', ion_logout, name='ion_logout'),
]