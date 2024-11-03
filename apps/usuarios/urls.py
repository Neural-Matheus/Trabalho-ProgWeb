from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('chat/', views.iniciar_streamlit, name='chat'),
    path("users/", views.user_list, name="user_list"),
    path("users/delete/<int:user_id>/", views.delete_user, name="delete_user")
]
