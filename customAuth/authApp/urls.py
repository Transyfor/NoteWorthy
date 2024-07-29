from django.urls import path
from . import views
app_name = 'authApp'
urlpatterns = [
    path('register/', views.register2, name='register'),
    path('login/',views.login,name='login'),
    path('home/', views.home, name='home'),
    path('logout/',views.logout, name='logout'),
    path("delete/<int:sticky_id>", views.deleteSticky, name='delete_sticky'),
]