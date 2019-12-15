from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserSignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from users.models import Profile
from django.contrib.auth.decorators import login_required
import json

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        
        form = UserSignUpForm(request.POST)
        
        if form.is_valid():
            
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('users/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return redirect('email')
    else:
        form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def activate_account(request, uidb64, token):
    
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
       
        return redirect('home')
    
    else:
        user.is_active = True
        user.save()
        return redirect('home')

@login_required()
def profile_solde(request):
    
    return render(request,'users/solde.html')

@login_required()
def change_password(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Votre mot de passe a été changé avec succés!')
            return redirect('home')
        else:
            messages.error(request, 'Les mots de passes ne correspondent pas.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'users/password_change.html', {'form': form})


#c'est un sms de confirmation pour l'activation d'un compte
def email_send(request):
    return render(request,'users/email_send.html')

#l'invalidation de lien d'activation 
def active_link(request):
    return render(request,'users/active_link.html')

def about(request):
    return render(request,'users/about.html')