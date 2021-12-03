from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.views.decorators.csrf import csrf_exempt,csrf_protect

@csrf_exempt
def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password=  request.POST["password"]
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print("User does not exists ", e)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            print("username or password is incorrect", "Your password can’t be entirely numeric.") 
    return render(request, "users/login-register.html")

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