from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *


# Create your views here.
def Homepage(request):
    # get all the items under category
    category = Category.objects.filter(status=0)
    # creates a context with category
    context = {'category': category}
    return render(request, 'home.html', context)


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'username or password entered is incorrect')
            return redirect('/login/')

    else:
        return render(request, 'login.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        if (User.objects.filter(username=username).exists()):
            messages.info(request, "Username already taken")
            return redirect('/register/')
        elif (User.objects.filter(email=email).exists()):
            messages.info(request, "User with this email already exists")
            return redirect('/register/')
        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.save()
            messages.info(request, "You successfully Registered")
            return redirect('/login/')
    else:
        return render(request, 'reg.html')


def profile(request):
    return render(request, 'profile.html')


def Logout(request):
    auth.logout(request)
    return redirect('/')


def payment(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        nick_name = request.POST['nick_name']
        email = request.POST['email']
        day = request.POST['day']
        month = request.POST['month']
        year = request.POST['year']
        amount = request.POST['amount']
        p = Payment(
            full_name=full_name,
            nick_name=nick_name,
            email=email,
            amount=amount,
        )
        p.save()
        messages.info(request, "Payment Added")
        return redirect('/')
    else:
        return render(request, 'payment.html')


def feedback(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['mailid']
        country = request.POST['country']
        feedback_text = request.POST['subject']
        f = Feedback(
            first_name=first_name,
            last_name=last_name,
            email=email,
            country=country,
            feedback_text=feedback_text,
        )
        f.save()
        messages.info(request, "User Feedback Added")
        return redirect('/')
    else:
        return render(request, 'feedback.html')


def collectionsview(request, slug):
    if (Category.objects.filter(slug=slug, status=0)):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {'products': products, 'category': category}
        return render(request, "products/index.html", context)
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('/')

def custom_404(request,exception):
    return render(request,'error_404.html',status=404)

def productview(request, cate_slug, prod_slug):
    if Category.objects.filter(slug=cate_slug, status=0):
        if (Product.objects.filter(slug=prod_slug, status=0)):
            products = Product.objects.filter(slug=prod_slug, status=0).first()
            context = {'products': products}
        else:
            messages.warning(request, "No Such Product Found")
            return redirect('/')
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('/')
    return render(request, "products/display.html", context)
