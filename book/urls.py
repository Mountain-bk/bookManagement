from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_action, name='logout'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('book-shelf/', views.book_shelf_view, name='book shelf'),
    path('book-register/', views.book_register_view, name='book register'),
    path('book-edit/<int:id>', views.book_edit_view, name='book edit'),
    path('book-detail/<int:id>', views.book_detail_view, name='book detail'),
]
