from django.shortcuts import render

VIEW_PARTIE = 1
VIEW_INVITATION = 2
VIEW_NOTIFICATION = 3
VIEW_STATISTIQUE = 4
VIEW_PROFIL = 5



def partie(request):
    
    context = {"ACTIVE_VIEW":VIEW_PARTIE}
    return render(request, "pages/morpion/partie.html",context)

def invitation(request):
    
    context = {"ACTIVE_VIEW":VIEW_INVITATION}
    return render(request, "pages/morpion/invitation.html",context)

def notification(request):
    
    context = {"ACTIVE_VIEW":VIEW_NOTIFICATION}
    return render(request, "pages/morpion/notification.html",context)

def statistique(request):
    
    context = {"ACTIVE_VIEW":VIEW_STATISTIQUE}
    return render(request, "pages/morpion/statistique.html",context)

def profil(request):
    
    context = {"ACTIVE_VIEW":VIEW_PROFIL}
    return render(request, "pages/morpion/profil.html",context)


def signIn(request):
    return render(request, "pages/auth/sign-in.html")


def signUp(request):
    return render(request, "pages/auth/sign-up.html")


def global_vars(request):
    
    return {
        'VIEW_PARTIE' : VIEW_PARTIE,
        'VIEW_INVITATION' : VIEW_INVITATION,
        'VIEW_NOTIFICATION' : VIEW_NOTIFICATION,
        'VIEW_STATISTIQUE' : VIEW_STATISTIQUE,
        'VIEW_PROFIL' : VIEW_PROFIL,
    }
     
 