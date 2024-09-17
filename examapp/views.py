from django.shortcuts import render, get_object_or_404
import random
from .models import *
from .forms import *
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Game
from .forms import GameForm

# Create your views here.


def index(request):
    return render(request, 'index.html')

class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class UserLoginView(LoginView):
    template_name='login.html'


def logout_user(request):
    logout(request)
    return redirect("/")

def all_games(request):
    games = Game.objects.all()
    return render(request, 'all_games.html', {'games': games})

def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return render(request, 'game_detail.html', {'game': game})

def games_by_platform(request, platform):
    games = Game.objects.filter(platform=platform)
    context = {
        'games': games,
        'platform': platform
    }
    return render(request, 'games_by_platform.html', context)


from django.shortcuts import redirect, render, get_object_or_404
from .models import Game

def add_to_basket(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            if game.number_in_stock > 0:
                quantity_to_add = int(request.POST.get('quantity', 1))  # Get quantity from the form
                if quantity_to_add <= game.number_in_stock:
                    # Check if the game is already in the user's basket
                    if user.basket.filter(id=game_id).exists():
                        # Game already in basket, increase quantity instead of adding again
                        basket_item = user.basket.get(id=game_id)
                        basket_item.quantity += quantity_to_add
                        basket_item.save()
                    else:
                        # Add the game to the user's basket
                        user.basket.add(game, through_defaults={'quantity': quantity_to_add})
                    # Decrease the stock count
                    game.number_in_stock -= quantity_to_add
                    game.save()
                    return redirect('view_basket')
                else:
                    return render(request, 'out_of_stock.html', {'game': game})
            else:
                return render(request, 'out_of_stock.html', {'game': game})
        else:
            return redirect('login')
    else:
        return render(request, 'add_to_basket.html', {'game': game})


def view_basket(request):
    if request.user.is_authenticated:
        user = request.user
        basket_items = user.basket.all()
        total_price = sum(item.price for item in basket_items)
        return render(request, 'view_basket.html', {'basket': basket_items, 'total_price': total_price})
    else:
        return redirect('login')


def upload_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_games')
    else:
        form = GameForm()
    return render(request, 'upload_game.html', {'form': form})
