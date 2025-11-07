from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SignUpForm
from .models import User

class SimpleLoginView(LoginView):
    template_name = 'accounts/login.html'

def logout_view(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_login_redirect')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def post_login_redirect(request):
    if request.user.role == 'lawyer':
        return redirect('lawyer_dashboard')
    return redirect('user_home')

@login_required
def profile(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user: User = request.user  # type: ignore
        # Upload image
        if action == 'upload_image' and 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
            user.save(update_fields=['profile_image'])
            return redirect('profile')
        # Update lawyer fields
        if action == 'update_profile' and user.role == 'lawyer':
            user.bio = request.POST.get('bio', '')
            
            # Handle cases_fought
            cases_fought_val = request.POST.get('cases_fought')
            if cases_fought_val and cases_fought_val.strip():
                try:
                    user.cases_fought = int(cases_fought_val)
                except (TypeError, ValueError):
                    user.cases_fought = None
            else:
                user.cases_fought = None
            
            # Handle cases_won
            cases_won_val = request.POST.get('cases_won')
            if cases_won_val and cases_won_val.strip():
                try:
                    user.cases_won = int(cases_won_val)
                except (TypeError, ValueError):
                    user.cases_won = None
            else:
                user.cases_won = None
            
            # Handle fee
            fee_val = request.POST.get('fee')
            if fee_val and fee_val.strip():
                try:
                    user.fee = float(fee_val)
                except (TypeError, ValueError):
                    user.fee = None
            else:
                user.fee = None
            
            user.save(update_fields=['bio', 'cases_fought', 'cases_won', 'fee'])
            return redirect('profile')
    return render(request, 'accounts/profile.html')