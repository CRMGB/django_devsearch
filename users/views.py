from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from .forms import CustomUserCreation

@csrf_exempt
def login_page(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password=  request.POST["password"]
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            messages.error(request, "User does not exists ")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "username or password is incorrect") 
    return render(request, "users/login-register.html")

def logout_user(request):
    logout(request)
    messages.error(request, "User successfully loged out")
    return redirect("login")

def register_user(request):
    page = "register"
    form = CustomUserCreation()
    if request.method == "POST":
        form = CustomUserCreation(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User account has been created")
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "An error has occurred during the registration")
    context = {"page": page, "form":form }
    return render(request, "users/login-register.html", context)

def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk) 
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")
    context = {'profile': profile, "top_skills": top_skills, "other_skills": other_skills}
    return render(request, "users/user-profile.html", context)