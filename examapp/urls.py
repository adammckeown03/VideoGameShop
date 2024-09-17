from django.urls import path
from . import views
from .forms import * # add o imports at the top of the file

urlpatterns = [
    path('', views.all_games, name='all_games'),
    path('register/', views.UserSignupView.as_view(), name="register"),
    path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),
    path('logout/', views.logout_user, name="logout"),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('games/platform/<str:platform>/', views.games_by_platform, name='games_by_platform'),
    path('add_to_basket/<int:game_id>/', views.add_to_basket, name='add_to_basket'),
    path('view_basket/', views.view_basket, name='view_basket'),
    path('upload_game/', views.upload_game, name='upload_game'),   
]