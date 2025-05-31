from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/toggle/<int:book_id>/', views.toggle_read, name='toggle_read'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('favourite/<int:book_id>/', views.toggle_favourite, name='toggle_favourite'),


    path('genres/', views.genres, name='genres'),
    path('blog/', views.blog, name='blog'),
    path('reviews/', views.reviews, name='reviews'),
    path('myshelf/', views.myshelf, name='myshelf'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
