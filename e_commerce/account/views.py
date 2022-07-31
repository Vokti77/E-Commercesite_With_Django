from django.shortcuts import render
from django.http import HttpResponse
from account.forms import RegistrationForm
# Authentication Building Function import
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


def register(request):
    if request.user.is_authenticated:
        return HttpResponse("You Are Authenticate!")
    else:
        form = RegistrationForm
        if request.method == 'post' or request.method == 'POST':
            form = RegistrationForm(request.POST)

            if form.is_valid():
                form.save()
                return HttpResponse("Account bas been Created!")

        contex = {
            'form': form
        }

    return render(request, 'accounts/register.html', contex)


def Customerlogin(request):
    if request.user.is_authenticated:
        return HttpResponse("You are Login!")
    else:
        if request.method == 'post' or request.method == 'POST':
            username = request.POST.get('username')  # get value from template using POST.get method
            password = request.POST.get('password')
            customer = authenticate(request, username=username, password=password)

            if customer is not None:
                login(request, customer)
                return HttpResponse("You are login successfully! ")
            else:
                return HttpResponse("Error 404!")

    return render(request, 'accounts/login.html')