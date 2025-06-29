from django.urls import path
from .views import home, signup_view, login_view, logout_view, add_note_view, my_notes_view, edit_note_view, delete_note_view

urlpatterns = [
    path('', home, name='home'),
    path('signup', signup_view, name='signup'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('add/note', add_note_view, name='add_note'),
    path('my/notes/', my_notes_view, name='my_notes'),
    path('my/notes/edit/<int:pk>/', edit_note_view, name='edit_note'),
    path('my/notes/delete/<int:pk>/',delete_note_view, name='delete_note'),

]