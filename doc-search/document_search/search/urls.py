from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_document, name='upload_document'),
    path('search/', views.search_document, name='search_document'),
    path('delete/<int:document_id>/', views.delete_document, name='delete_document'),

]
