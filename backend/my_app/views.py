from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .decorators import anonymous_required

@login_required
def index(request):
    return render(request, 'index.html')

@anonymous_required
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful sign-up
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
