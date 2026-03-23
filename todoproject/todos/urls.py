from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('toggle/<int:pk>/', views.toggle, name='toggle'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/new/', views.note_create, name='note_create'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('search/', views.search, name='search'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
