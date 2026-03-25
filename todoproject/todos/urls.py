from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('toggle/<str:pk>/', views.toggle, name='toggle'),
    path('delete/<str:pk>/', views.delete, name='delete'),
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/new/', views.note_create, name='note_create'),
    path('notes/<str:pk>/', views.note_detail, name='note_detail'),
    path('notes/<str:pk>/delete/', views.note_delete, name='note_delete'),
    path('search/', views.search, name='search'),
    path('files/', views.files_list, name='files_list'),
    path('files/upload/', views.file_upload, name='file_upload'),
    path('files/<str:pk>/download/', views.file_download, name='file_download'),
    path('files/<str:pk>/delete/', views.file_delete, name='file_delete'),
    path('code/', views.code_list, name='code_list'),
    path('code/new/', views.code_create, name='code_create'),
    path('code/<str:pk>/', views.code_detail, name='code_detail'),
    path('code/<str:pk>/delete/', views.code_delete, name='code_delete'),
    path('links/', views.links_list, name='links_list'),
    path('links/add/', views.link_add, name='link_add'),
    path('links/<str:pk>/delete/', views.link_delete, name='link_delete'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
