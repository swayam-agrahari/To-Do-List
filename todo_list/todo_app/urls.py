# todo_list/todo_app/urls.py
from django.urls import path
from todo_app import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    
    
    path('', views.LoginPage, name='login'),
    path('signup/', views.SignupPage, name='signup'),
    path('logout/', views.LogoutPage, name='logout'),

    path(
        "home/", views.ListListView.as_view(), name="index"
        ),
    
    path("list/<int:list_id>/", views.ItemListView.as_view(), name="list"),
    # CRUD patterns for ToDoLists
    path("list/add/", views.ListCreate.as_view(), name="list-add"),
    path(
        "list/<int:pk>/delete/", views.ListDelete.as_view(), name="list-delete"
    ),
    # CRUD patterns for ToDoItems
    path(
        "list/<int:list_id>/item/add/",
        views.ItemCreate.as_view(),
        name="item-add",
    ),
    path(
        "list/<int:list_id>/item/<int:pk>/",
        views.ItemUpdate.as_view(),
        name="item-update",
    ),
    path(
        "list/<int:list_id>/item/<int:pk>/delete/",
        views.ItemDelete.as_view(),
        name="item-delete",
    ),
]