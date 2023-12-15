from django.shortcuts import render,redirect

from Morpion.models import Game, GameConfig, User, get_game_config_or_create
from Morpion.utils import isEmpty

VIEW_PARTIE = 1
VIEW_INVITATION = 2
VIEW_NOTIFICATION = 3
VIEW_STATISTIQUE = 4
VIEW_PROFIL = 5
 
def partie(request):
    if not request.session.has_key('isLogin'):
        return redirect("signin")  
    
    games =  Game.objects.filter()
    context = {"ACTIVE_VIEW":VIEW_PARTIE,"games":games}
    return render(request, "pages/morpion/partie/home.html",context)


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
  

        if visibility=="PRIVATE" and isEmpty(access_code):
             error = True
             message = "Veuillez donner un code d'access pour cette partie"

        

        if not error:
            if isEmpty(title):
                title = "Partie "+str(Game.objects.filter(owner=User(user_id)).count() + 1)

            game = Game(title=title,visibility=visibility,access_code=access_code,config=get_game_config_or_create(size,alignment),owner=User(user_id))
            game.save()
            error = False
            success = True
            message = "La partie a ete cree avec success"
 
        
    context = {"ACTIVE_VIEW":VIEW_PARTIE, "error": error,"success":success,"message":message}
    return render(request, "pages/morpion/partie/creation.html",context)

def invitation(request):
    
    if not request.session.has_key('isLogin'):
        return redirect("signin")   
        
    context = {"ACTIVE_VIEW":VIEW_INVITATION}
    return render(request, "pages/morpion/invitation.html",context)

def notification(request):
    
    if not request.session.has_key('isLogin'):
        return redirect("signin")   
            
    context = {"ACTIVE_VIEW":VIEW_NOTIFICATION}
    return render(request, "pages/morpion/notification.html",context)

def statistique(request):
    
    if not request.session.has_key('isLogin'):
        return redirect("signin")   
            
    context = {"ACTIVE_VIEW":VIEW_STATISTIQUE}
    return render(request, "pages/morpion/statistique.html",context)



def profil(request):
    
    if not request.session.has_key('isLogin'):
        return redirect("signin")   
            
    context = {"ACTIVE_VIEW":VIEW_PROFIL}
    return render(request, "pages/morpion/profil.html",context)


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
    
    return render(request, "pages/auth/sign-in.html",result)


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

    return render(request, "pages/auth/sign-up.html",result)

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
        'VIEW_PARTIE' : VIEW_PARTIE,
        'VIEW_INVITATION' : VIEW_INVITATION,
        'VIEW_NOTIFICATION' : VIEW_NOTIFICATION,
        'VIEW_STATISTIQUE' : VIEW_STATISTIQUE,
        'VIEW_PROFIL' : VIEW_PROFIL,
    }
     
 