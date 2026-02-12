from django.urls import path
from . import views

app_name = 'rbac_app'

urlpatterns = [
    # Auth only
    path('', views.index, name='index'),
    path('register/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]