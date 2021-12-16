from django.forms import forms
from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .forms import CustomUserCreation, ProfileForm, SkillForm


@csrf_exempt
def login_page(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
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
    messages.info(request, "User successfully loged out")
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
            return redirect("edit-account")
        else:
            messages.error(request, "An error has occurred during the registration")
    context = {"page": page, "form": form}
    return render(request, "users/login-register.html", context)


def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")
    context = {
        "profile": profile,
        "top_skills": top_skills,
        "other_skills": other_skills,
    }
    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form_prof = ProfileForm(instance=profile)
    if request.method == "POST":
        form_prof = ProfileForm(request.POST, request.FILES, instance=profile)
        if form_prof.is_valid():
            form_prof.save()
            return redirect("account")
    context = {"form": form_prof}
    return render(request, "users/profile_form.html", context)

@login_required(login_url="login")
def create_skill(request):
    profile = request.user.profile
    form_skill = SkillForm()
    if request.method == "POST":
        form_skill = SkillForm(request.POST)
        if form_skill.is_valid():
            skill = form_skill.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill created successfully")
            return redirect("account")
    context = {"form": form_skill}
    return render(request, "users/skill-form.html", context)


@login_required(login_url="login")
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form_skill = SkillForm(instance=skill)
    if request.method == "POST":
        form_skill = SkillForm(request.POST, instance=skill)
        if form_skill.is_valid():
            form_skill.save()
            messages.success(request, "Skill edited successfully")            
            return redirect("account")
    context = {"form": form_skill}
    return render(request, "users/skill-form.html", context)

@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill deleted successfully")
        return redirect("account")
    context = {"object":skill}
    return render(request, "delete_template.html", context)