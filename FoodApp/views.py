from django.contrib import admin
from django.contrib.auth.password_validation import password_changed
from django.core import exceptions
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import Cart, UserProfile, Food, OrderSummary, Orders
from .forms import FoodForm, UserForm, UserProfileForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login,logout
from django.db.models import Sum
from django.contrib.auth.decorators import user_passes_test
import razorpay
from FoodOdering.settings import PASSWORD, RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY, Email
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
import smtplib as s
object = s.SMTP('smtp.gmail.com',587)
object.starttls()
object.login(Email, PASSWORD)

# Create your views here.
def is_admin(user):
    return user.groups.filter(name='admin').exists()

def is_customer(user):
    return user.groups.filter(name='customer').exists()


@user_passes_test(is_admin)
def AddFood(request):
    form=FoodForm()
    if request.method=="POST":
        form=FoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            print("success")
    return render(request, 'FoodApp/addfood.html',{'form':form})

def showFood(request):
    food=Food.objects.all()
    return render(request, 'FoodApp/menu.html',{'foodlist':food})

def updateFoods(request, id):
    status=request.user.groups.filter(name='admin').exists()
    print(status)
    if status:
        food=Food.objects.get(id=id)
        if request.method=='POST':
            form=FoodForm(request.POST, request.FILES, instance=food)  
            if form.is_valid():
                form.save()
                return redirect('/menu/')
        return render(request, 'FoodApp/updateMenu.html',{'food':food})
    else:
        return redirect('/login/')

def deleteFood(request, id):
    food=Food.objects.get(id=id)
    food.delete()
    return redirect('/menu/')

def addUser(request):
    uform = UserForm()
    form = UserProfileForm()
    if request.method=='POST':
        role=request.POST['role']
        uform = UserForm(request.POST)
        form = UserProfileForm(request.POST)
        if uform.is_valid() and form.is_valid():
            uobj=uform.save(commit=True)
            uobj.set_password(uobj.password)
            uobj.save()
            userobj = form.save(commit=False)
            userobj.user = uobj
            userobj.save()
            if role=='customer':
                cust=Group.objects.get(name='customer')  
                uobj.groups.add(cust)
            elif role=='admin':
                admin=Group.objects.get(name='admin')  
                uobj.groups.add(admin)                              
    return render(request, 'FoodApp/register.html', {'uform':uform,'form':form})

def showUser(request):
    user=UserProfile.objects.all()
    print(user)
    return render(request, 'FoodApp/customerlist.html',{'user':user})

def EditUserProfile(request):
    pass

def updateFood(request):
    pass

def loginuser(request):
    form=AuthenticationForm()
    if request.method=="POST":
        uname=request.POST['username']
        pwd=request.POST.get('password')
        user=authenticate(username=uname, password=pwd)
        print(user)
        if user!=None:
            login(request, user)
            return redirect('/menu/')
        else:
            msg="invalid username and password"
            return render(request, "FoodApp/login.html",{'form':form, 'msg':msg})
    return render(request, "FoodApp/login.html",{'form':form})

def logoutuser(request):
    logout(request)     #internall it'll delete the session object
    print(request)
    return redirect('/index/')

def index(request):
    return render(request, 'FoodApp/index.html')

def showUserProfile(request):
    currentuser =  request.user
    # print(currentuser)
    userobject = UserProfile.objects.get(user=currentuser)
    groupobj = str(Group.objects.get(user=currentuser))
    print(groupobj)
    return render(request, 'FoodApp/userprofile.html', {'user':userobject, 'role':groupobj})


#username=fareen1234 password=fareen
def editUserProfile(request):
    currentuser =  request.user
    print(currentuser)
    data = UserProfile.objects.get(user=currentuser)
    data1 = User.objects.get(username=currentuser)
    if request.method == 'POST':
        print(request.POST)
        uform = UserForm(request.POST, instance=data1)  #if we dont pass instance it'll create new object
        form = UserProfileForm(request.POST, instance=data)
        print(uform, form)
        if uform.is_valid() and form.is_valid():
            print(uform, form)
            uobj=uform.save(commit=True)
            uobj.save()
            userobj = form.save(commit=False)
            userobj.user = uobj
            userobj.save()
    return redirect('/index/')

def addtocart(request):
    print(request.GET)
    fid = request.GET['foodid']
    price = request.GET['price']
    customer = request.user
    fobj = Food.objects.get(id=fid)
    Cart(customer=customer, foodobj=fobj, price=price).save()
    return redirect('/menu/')

def showcart(request):
    data = Cart.objects.filter(customer=request.user)
    # flag=data.exists()
    if request.method=="POST":
        totalbill=request.POST.get('totalamount')
        print(totalbill)
        customer = UserProfile.objects.get(user=request.user)

        order_amount = int(totalbill)*100
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {'Shipping address': 'Bommanahalli, Bangalore'}   # OPTIONAL

        orderobject=client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes))
        orderid=orderobject['id']
        return render(request, 'FoodApp/payment.html', {'customer':customer, 'amount':order_amount,'oid':orderid, 'apikey':RAZORPAY_API_KEY})

    return render(request, 'FoodApp/mycart.html', {'items':data})

# def paymentView(request):


def updateCart(request):
    if request.method=="POST":
        print(request.POST)
        q=request.POST['qnt']
        price=request.POST['price']
        id=request.POST['id']
        totalprice=int(q)*float(price)
        Cart.objects.filter(id=id).update(qnt=q, price=totalprice)
        data=Cart.objects.filter(customer=request.user).aggregate(Sum('price'))
        totalamount=data['price__sum']
        print(totalamount)
    return JsonResponse({'response':True,'totalprice':totalprice,'amount':totalamount})

def deleteCart(request, id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    return redirect('/mycart/')

def addOrders(request):
    totalbill=request.POST['totalamount']
    totalbill=int(totalbill)/100
    crntUser=request.user
    ordersumaryobje=OrderSummary.objects.create(totalamount=totalbill, customer=crntUser)
    ordersumaryobje.save()
    subject='Order has been placed : '
    body="Thank you for you order your order will deliver soon"
    msg='Subject :{}\n\n{}'.format(subject,body)
    object.sendmail(Email,crntUser.email,msg)
    object.quit()
    try:
        data=Cart.objects.filter(customer=crntUser)
        for item in data:
            ordobj=Orders(ordersobj=ordersumaryobje, foodobj=item.foodobj, quantity=item.qnt, totalprice=item.price)
            ordobj.save()
            item.delete()
        return render(request,"FoodApp/index.html", {'success':'order has been placed'})
    except Exception:
        return render(request, 'FoodApp/index.html',{'msg':'some error occured'})

def showorders(request):
    obj=OrderSummary.objects.filter(customer=request.user)
    items=[]
    # Orders.objects.filter
    for i in obj:
        data=Orders.objects.filter(ordersobj=i)
        for object in list(data):
            items.append(object)
    print(items)
    return render(request, "FoodApp/orderhistory.html",{'data':items,'ordersobj':obj})

#Adding payment gateway
