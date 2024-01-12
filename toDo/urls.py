from django.urls import path
from . import views

urlpatterns = [
    path('author/', views.author),
    # Create
    path('create_list/<str:name>', views.create_list),
    path('create_category', views.create_category),
    path('create_todo/<int:category_id>/<int:group_id>', views.create_toDo),
    # Read
    path('read_list/<str:name>', views.read_list),
    path('read_category/<int:id>', views.read_category),
    path('read_todo/<int:id>', views.read_todo),
    path('get_lists/', views.get_lists),
    path('get_categories/', views.get_categories),
    path('get_todos/', views.get_todos),
    path('lists/', views.show_lists),
    path('categories/', views.show_categories),
    path('todos/', views.show_todos),
    path('list/<int:id>', views.show_list),
    path('category/<int:id>', views.show_category),
    path('todo/<int:id>', views.show_toDo),
    path('search_lists', views.search_lists, name='search_lists'),
    path('search_categories', views.search_categories, name='search_categories'),
    path('search_todos', views.search_todos, name='search_todos'),
    # Update
    path('update_list/<str:name>/<str:newName>', views.update_list),
    path('update_category/<int:id>', views.update_category),
    path('update_todo/<int:id>', views.update_toDo),
    # Delete
    path('delete_list/<str:name>', views.delete_list),
    path('delete_category/<int:id>', views.delete_category),
    path('delete_todo/<int:id>', views.delete_toDo),
]
