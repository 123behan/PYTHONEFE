from http import HTTPStatus
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Meal, OrderTransaction
from django.views import View
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login, logout


class IndexView(View):
    def get(self, request):
        meals = []
        temp_list = []
        all_meals = Meal.objects.all()

        for cnt in range(all_meals.count()):
            temp_list.append(all_meals[cnt])

            if (cnt + 1) % 3 == 0 and cnt + 1 > 2:
                meals.append(temp_list)
                temp_list = []

        if temp_list:
            meals.append(temp_list)

        context = {
            'meals': meals,
        }
        return render(request, 'restaurant/index.html', context)


class OrderView(View):
    def get(self, request, pk=None):
        if pk:
            got_meal = Meal.objects.filter(id=pk).last()

            if got_meal and got_meal.stock > 0:
                OrderTransaction.objects.create(
                    meal=got_meal,
                    customer=request.user,
                    amount=got_meal.price
                )
                got_meal.stock -= 1
                got_meal.save()
                return redirect('index')

            return HttpResponse(HTTPStatus.BAD_REQUEST)


class DetailsView(View):
    def get(self, request):
        transactions = OrderTransaction.objects.filter(customer=request.user)

        context = {
            'transactions': transactions,
        }
        return render(request, 'restaurant/details.html', context)

class CustomLoginView(View):
    form_class =UserLoginForm
    template_name='restaurant/login.html'

    def get(self,request):
        form = self.form_class()
        form.fields['password'].widget.attrs['placeholder'] = 'Your password'

        context ={
            'login_form': form,
        }
        return render(request=request,template_name=self.template_name,context=context)
    def post(self,request):
        form =self.form_class(request.POST,request.FILES)

        if form.is_valid():
            username=form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            authenticateUser = authenticate(request,username=username,password=password)

            if authenticateUser is not None:
                login(request,authenticateUser)
                return redirect('details')
            form.add_error('username','Wrong Username and password')
            form.add_error('username','Wrong Username and password')
        context={
            'login_form': form,

        }
        return render(request=request,template_name=self.template_name,context=context)
def login_user(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            authenticateUser = authenticate(request, username=username, password=password)
            if authenticateUser is not None:
                login(request, authenticateUser)
                return redirect('details')

            login_form.add_error('username', 'Wrong username or password!')
            login_form.add_error('password', 'Wrong username or password!')
    else:
        login_form = UserLoginForm()
        login_form.fields['password'].widget.attrs['placeholder'] = 'Your Password'

    context = {
        'login_form': login_form,
    }
    return render(request, 'restaurant/login.html', context)



def logout_user(request):
    logout(request)
    return redirect('index')
