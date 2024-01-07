from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from Morpion.models import Game, GameConfig,create_or_inc_score, User, get_game_config_or_create
from Morpion.utils import isEmpty,has_winner
 

VIEW_PARTIE = 1
VIEW_INVITATION = 2
VIEW_NOTIFICATION = 3
VIEW_STATISTIQUE = 4
VIEW_PROFIL = 5


def partie_auth(request, game_id="game_id"):

    if not request.session.has_key('isLogin'):
        return redirect("signin")

    result = {'error': False}
    if request.method == 'POST':
        game = Game.objects.get(id=game_id)
        user_id = request.session["user"]['id']
        access_code = request.POST["access_code"]
        if game.access_code == access_code:
            print("Joueur authentifier")
            result = {
                "ACTIVE_VIEW": VIEW_PARTIE, 
                "game": game,
            }
        else:
            result = {
                'error': True,
                'message': "Code incorrect",
                "ACTIVE_VIEW": VIEW_PARTIE, 
                "game": game,
            }
    return render(request, "pages/morpion/partie/game-auth.html", result)


def partie(request):
    if not request.session.has_key('isLogin'):
        return redirect("signin")

    games = Game.objects.filter(~Q(status="FINISHED")).order_by("-created_at")
    context = {"ACTIVE_VIEW": VIEW_PARTIE, "games": games}
    return render(request, "pages/morpion/partie/home.html", context)


def make_move(request, game_id="game_id"):

    if not request.session.has_key('isLogin'):
        return redirect("signin")

    row = int(request.POST.get('row'))
    col = int(request.POST.get('col'))
    game = Game.objects.get(id=game_id)
    user_id = request.session["user"]['id']
    values_list = list(game.symbol.values())
    
    
    
    response_data = {}
    
    if game.status=="FINISHED":
        response_data["message"]= "Cette partie est terminee"
        response_data["is_error"]=True 
        return JsonResponse(response_data, status=403)
    
    if len(values_list) != 2 :
        response_data["message"]= "Il faut deux joueurs pour commencer la partie"
        response_data["is_error"]=True 
        return JsonResponse(response_data, status=403)
    
    if game.current_player != User(user_id):
        response_data["message"]= "It's not your turn"
        response_data["is_error"]=True 
 

        return JsonResponse(response_data, status=403)

    if game.board[row][col] is None:  
        game.board[row][col] = game.current_player.id
        
        if has_winner(game):
            game.status="FINISHED"
            create_or_inc_score(game) 
        else:
            game.current_player = game.player2 if game.current_player == game.player1 else game.player1
        
        game.save()
        
 

        return JsonResponse({})
    else:
        response_data = {
            'message': 'Cell already taken. Try again.',
            "is_error": True
        }

        return JsonResponse(response_data, status=400)





    
def play_game(request, game_id="game_id"):

    if not request.session.has_key('isLogin'):
        return redirect("signin")

    game = Game.objects.get(id=game_id)
    user_id = request.session["user"]['id']
 
    #Verifie que le partie existe
    if game:
        context = {
                    "ACTIVE_VIEW": VIEW_PARTIE, 
                    "game": game,
                    "size": range(game.config.grid_size),
                    "hasSymbol" : False if not game.symbol else str(user_id) in game.symbol 
                }
        
        ## Mise a jour des symboles pour la partie
        if request.method == 'POST': 
            symbol = request.POST["symbol"]  
            values_list = list(game.symbol.values())
            if symbol in values_list:
                context["has_error"] = True  
                context["symbol_icon"] = symbol  
                return render(request, "pages/morpion/partie/play.html", context)
            
            game.symbol[user_id]=symbol
            game.save()
            return redirect("play_game",game_id=game_id)
 
        if game.visibility == "PRIVATE" and game.owner.id != user_id:  # Pour les parties privees

            return render(request, "pages/morpion/partie/game-auth.html", context)


        
        if game.owner.id != user_id and not game.player2:
            game.player2 = User(user_id)
            print("Register Player2 = ", user_id)
            game.save()
            
        return render(request, "pages/morpion/partie/play.html", context)

    return redirect("partie")


def creation_partie(request):

    if not request.session.has_key('isLogin'):
        return redirect("signin")

    error = False
    success = False
    message = ""
    if request.method == 'POST':
        user_id = request.session["user"]['id']
        title = request.POST["title"]
        visibility = request.POST["visibility"]
        size = request.POST["size"] 
        alignment = request.POST["alignment"]
        access_code = request.POST["access_code"]

        if visibility == "PRIVATE" and isEmpty(access_code):
            error = True
            message = "Veuillez donner un code d'access pour cette partie"

        if not error:
            current_player = User(user_id)
            if isEmpty(title):
                title = "Partie " + str(Game.objects.filter(owner=current_player).count() + 1)
            size = int('0'+size)
            alignment = int('0'+alignment)
          
            game = Game(title=title,
                        board=[[None] * size for _ in range(size)],
                        visibility=visibility,
                        access_code=access_code,
                        config=get_game_config_or_create(size, alignment),
                        owner=current_player,
                        current_player=current_player,
                        player1=current_player,
                        symbol={})
           
            game.save()
            return redirect("partie") 

    context = {
                "ACTIVE_VIEW": VIEW_PARTIE, 
               "error": error,
               "success": success, 
               "message": message
            }
    return render(request, "pages/morpion/partie/creation.html", context)


def invitation(request):

    if not request.session.has_key('isLogin'):
        return redirect("signin")

    context = {"ACTIVE_VIEW": VIEW_INVITATION}
    return render(request, "pages/morpion/invitation.html", context)


def notification(request):

    if not request.session.has_key('isLogin'):
        return redirect("signin")

    context = {"ACTIVE_VIEW": VIEW_NOTIFICATION}
    return render(request, "pages/morpion/notification.html", context)


def statistique(request):

    if not request.session.has_key('isLogin'):
        return redirect("signin")

    context = {"ACTIVE_VIEW": VIEW_STATISTIQUE}
    return render(request, "pages/morpion/statistique.html", context)


def profil(request):
    #Game.objects.all().delete()
    if not request.session.has_key('isLogin'):
        return redirect("signin")

    context = {"ACTIVE_VIEW": VIEW_PROFIL}
    return render(request, "pages/morpion/profil.html", context)


def sign_in(request):
    if request.session.has_key('isLogin'):
        return redirect("partie")

    result = {'error': False}
    if request.method == 'POST':

        email = request.POST["email"]
        password = request.POST["password"]

        cnt = User.objects.filter(email=email, password=password).count()

        if cnt != 1:
            result = {
                'error': True,
                'message': "L'email ou le mot de pass n'est pas correct"
            }

        else:
            user = User.objects.get(email=email, password=password)
            request.session["user"] = {'id': user.id,
                                       'name': user.name, 'email': user.email}
            request.session["isLogin"] = True
            return redirect("partie")

    return render(request, "pages/auth/sign-in.html", result)


def sign_up(request):
    if request.session.has_key('isLogin'):
        return redirect("partie")
    result = {'error': False}
    if request.method == 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if isEmpty(name) or isEmpty(email) or isEmpty(password1) or isEmpty(password2):
            result = {
                'error': True,
                'message': "Veuillez remplir tous les champs"
            }

        if password1 != password2:
            result = {
                'error': True,
                'message': "Les deux mots de passes ne sont pas identique"
            }

        if not result['error']:
            nbr = User.objects.filter(email=email).count()

            if nbr > 0:
                result = {
                    'error': True,
                    'message': "L'adress mail est deja utiliser"
                }
            else:
                user = User(name=name, email=email, password=password1)
                user.save()
                result = {
                    'error': False,
                    'success': True,
                    'message': "Felicitation votre compte a ete cree !!!  connectez-vous a present"
                }

    return render(request, "pages/auth/sign-up.html", result)


def logout(request):
    if request.session.has_key('isLogin'):
        try:
            del request.session["user"]
            del request.session["isLogin"]

        except:
            pass
    return redirect("signin")


def global_vars(request):

    return {
        'VIEW_PARTIE': VIEW_PARTIE,
        'VIEW_INVITATION': VIEW_INVITATION,
        'VIEW_NOTIFICATION': VIEW_NOTIFICATION,
        'VIEW_STATISTIQUE': VIEW_STATISTIQUE,
        'VIEW_PROFIL': VIEW_PROFIL,
    }



