from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_action, name='logout'),
    path('mypage/', views.mypage_view, name='mypage'),
]
