from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path('add_author/', views.add_author, name='add-author'),
    path('add_quote/', views.add_quote, name='add-quote'),
    path('author/<int:author_id>/', views.author_detail, name='author-detail'),
    path('', views.quotes_list, name='quotes-list'),
]
