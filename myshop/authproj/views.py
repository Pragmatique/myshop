from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework_jwt.views import obtain_jwt_token,ObtainJSONWebToken

from .models import User
from .forms import UserRegistrationForm,UserLoginForm


# Create your views here.
def signing_up(request):

    user_form = UserRegistrationForm()

    context_dictionary = {
        "user_form": user_form,
    }

    if request.method=="POST":

        user_form=UserRegistrationForm(request.POST)

        if user_form.is_valid():

            new_user=User.objects.create_user(**user_form.cleaned_data)

            # user=authenticate(
            #     username=user_form.cleaned_data['username'],
            #     password=user_form.cleaned_data['password']
            # )
            #
            # login(request,user)

            return redirect('authproj:signing_in')

    return render(request, 'authproj/sign_up.html',context_dictionary)

def signing_in(request):

    login_form = UserLoginForm()

    context_dictionary = {
        "login_form": login_form,
    }

    if request.method == "POST":

        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():

            # user = login_form.save(commit=False)
            # user.set_password(login_form.cleaned_data['password'])
            # user.save()

            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password']
            )

            login(request, user)

            return redirect('shop:product_list')

    return render(request, 'authproj/sign_in.html', context_dictionary)


def signing_out(request):

    logout(request)