from datetime import datetime

from django.contrib.messages.storage import session
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.db.models import Q
from django.core import serializers

from .customer.models import Customer
from .menus.models import Menus
from .user.models import User
from .product.models import Product
from .order.models import Order


def redirect_to_login(request):
    return HttpResponseRedirect("/login-page")


def logout(request):
    request.session.clear()
    print("Logout ")
    print(request.session.get("user_info"))
    return HttpResponseRedirect("/login-page")


def login(request):
    user_info = request.session.get('user_info')
    if user_info is not None:
        return HttpResponseRedirect("/home")
    else:
        template = loader.get_template('login.html')
        return HttpResponse(template.render())


def validate_login(request):  # put application's code here
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST['password']
        user = User.objects.filter(email=email, password=password)
        if user is None or len(user) == 0:
            context = {
                "alert_type": "danger",
                'base_template': 'login.html',
                'message': 'Invalid Credentials: Please enter valid email id and password.'
            }
            return render(request, "alert.html", context)
        else:
            request.session['user_info'] = user.values_list("user_id", "email", "first_name",
                                                            "last_name", "role")[0]
            return HttpResponseRedirect("/home")


def register(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render())


def save_user(request):
    if request.method == 'POST':
        form = User()
        if request.POST.get("user_id") is not None:
            user_id = request.POST["user_id"]
        else:
            if len(User.objects.filter(email=request.POST["email"])) != 0:
                context = {
                    "alert_type": "danger",
                    'base_template': 'register.html',
                    'message': 'Email id already exists...'
                }
                return render(request, "alert.html", context)

            if len(User.objects.all()) != 0:
                user_id = User.objects.aggregate(Max('user_id')).get('user_id__max') + 1
            else:
                user_id = 1

        form.user_id = user_id
        form.email = request.POST["email"]
        form.first_name = request.POST["first_name"]
        form.last_name = request.POST["last_name"]
        form.password = request.POST["password"]
        form.role = request.POST["role"]
        print("form ")
        print(form.user_id)
        print(form.first_name)

        if request.POST.get("user_id") is not None:

            menus = get_menus_for_this_role(request)

            if len(User.objects.filter(~Q(email=request.session.get("user_info")[1])).filter(
                    email=request.POST["email"])) != 0:
                user_info = request.session.get('user_info')
                context = {
                    "alert_type": "danger",
                    'base_template': 'profile.html',
                    'message': 'Email id already exists...',
                    'role': user_info[4],
                    'first_name': user_info[2],
                    'last_name': user_info[3],
                    'email': user_info[1],
                    'user_id': user_info[0],
                    'menus': menus,
                    'full_name': user_info[2] + ' ' + user_info[3],
                }
                return render(request, "alert.html", context)

            form.save()
            user = User.objects.filter(user_id=request.POST['user_id'])
            request.session['user_info'] = user.values_list("user_id", "email", "first_name",
                                                            "last_name", "role")[0]
            user_info = request.session.get('user_info')
            context = {
                "alert_type": "success",
                'base_template': 'profile.html',
                'message': 'Update Successful: Profile updated successfully...',
                'role': user_info[4],
                'first_name': user_info[2],
                'last_name': user_info[3],
                'email': user_info[1],
                'user_id': user_info[0],
                'menus': menus,
                'full_name': user_info[2] + ' ' + user_info[3],
            }
        else:
            context = {
                "alert_type": "success",
                'base_template': 'register.html',
                'message': 'Registered Successful: Please enter your credentials to login.'
            }
            form.save()
        return render(request, "alert.html", context)


def save_customer(request):
    if request.method == 'POST':
        user_info = request.session.get('user_info')
        menus = get_menus_for_this_role(request)
        form = Customer()
        if request.POST.get("customer_id") is not None:
            customer_id = request.POST["customer_id"]
        else:
            if len(Customer.objects.filter(~Q(customer_id=request.POST["customer_id"])).filter(
                    email=request.POST["email"])) != 0:
                context = {
                    "alert_type": "danger",
                    'base_template': 'customers.html',
                    'message': 'Email id already exists...',
                    'menus': menus,
                    'full_name': user_info[2] + ' ' + user_info[3],
                    'role': user_info[4],
                    'customers': get_customers(),
                    'activeLink': 'Customers',
                }
                return render(request, "alert.html", context)

            if len(Customer.objects.all()) != 0:
                customer_id = Customer.objects.aggregate(Max('customer_id')).get('customer_id__max') + 1
            else:
                customer_id = 10000

        form.customer_id = customer_id
        form.email = request.POST["email"]
        form.name = request.POST["name"]
        form.address = request.POST["address"]
        form.contact_person = request.POST["contact_person"]
        form.contact_no = str(request.POST["contact_no"])

        if request.POST.get("customer_id") is not None:

            if len(Customer.objects.filter(~Q(customer_id=request.POST["customer_id"])).filter(
                    email=request.POST["email"])) != 0:
                customer_info = request.POST
                context = {
                    "alert_type": "danger",
                    'base_template': 'customers.html',
                    'message': 'Email id already exists...',
                    'role': user_info[4],
                    'name': customer_info["name"],
                    'address': customer_info["address"],
                    'email': customer_info["email"],
                    'customer_id': customer_info["customer_id"],
                    'contact_person': customer_info["contact_person"],
                    'contact_no': customer_info["contact_no"],
                    'menus': menus,
                    'full_name': user_info[2] + ' ' + user_info[3],
                    'customers': get_customers(),
                    'activeLink': 'Customers',
                }
                return render(request, "alert.html", context)

            form.save()

            user_info = request.session.get('user_info')
            context = {
                "alert_type": "success",
                'base_template': 'customers.html',
                'message': 'Update Successful: Customer details updated successfully...',
                'role': user_info[4],
                'menus': menus,
                'full_name': user_info[2] + ' ' + user_info[3],
                'customers': get_customers(),
                'activeLink': 'Customers',
            }
        else:

            context = {
                "alert_type": "success",
                'base_template': 'customers.html',
                'message': 'Successful: Customer added successfully....',
                'role': user_info[4],
                'menus': menus,
                'full_name': user_info[2] + ' ' + user_info[3],
                'customers': get_customers(),
                'activeLink': 'Customers',
            }
            form.save()
        return render(request, "alert.html", context)


def get_customers():
    return Customer.objects.all()


def get_all_customers(request):
    if request.method == 'GET':
        customers = serializers.serialize('json', Customer.objects.all())
        return HttpResponse(customers, content_type='application/json')


def get_customer_by_id(request):
    if request.method == 'POST':
        customer = serializers.serialize('json', Customer.objects.filter(customer_id=request.POST['customer_id']))
        return HttpResponse(customer, content_type='application/json')


def get_all_products(request):
    if request.method == 'GET':
        products = serializers.serialize('json', Product.objects.all())
        return HttpResponse(products, content_type='application/json')
    

def create_order(request):
    if request.method == 'POST':
        print(request.POST)
        form = Order()
        product = Product()

        product.name = request.POST['product_name']
        product.product_id = int(request.POST['product_id'])
        product.stock_qty = int(request.POST['stock_qty']) - int(request.POST['product_qty'])
        product.price = int(request.POST['price'])
        
        
        if request.POST.get("order_no"):
            form.order_no = request.POST["order_no"]
        elif len(Order.objects.all()) != 0:
            form.order_no = Order.objects.aggregate(Max('order_no')).get('order_no__max') + 1
            product.save()
        else:
            form.order_no = 1000000
            product.save()

        user_info = request.session.get('user_info')
        form.customer_id = int(request.POST['customer_id'])
        form.customer_name = request.POST['customer_name']
        form.product_id = int(request.POST['product_id'])
        form.product_name = request.POST['product_name']
        form.product_qty = request.POST['product_qty']
        form.contact_person = request.POST['contact_person']
        form.order_date = request.POST['order_date']
        form.status = request.POST['status']
        form.created_by_id = user_info[0]
        form.created_by = user_info[2] + ' ' + user_info[3]
        menus = get_menus_for_this_role(request)
        # try:
        form.save()
        context = {
            "alert_type": "success",
            'base_template': 'orders.html',
            'message': 'Successful: Order details saved successfully....',
            'role': user_info[4],
            'menus': menus,
            'full_name': user_info[2] + ' ' + user_info[3],
            # 'orders': get_orders(),
            'activeLink': 'Orders',
        }
        # except:
        #     context = {
        #         "alert_type": "error",
        #         'base_template': 'orders.html',
        #         'message': 'Failed: Failed to save order details....',
        #         'role': user_info[4],
        #         'menus': menus,
        #         'full_name': user_info[2] + ' ' + user_info[3],
        #         # 'orders': get_orders(),
        #         'activeLink': 'Orders',
        #     }

        return render(request, 'alert.html', context)


def get_all_orders(request):
    if request.method == 'GET':
        orders = serializers.serialize('json', Order.objects.all())
        return HttpResponse(orders, content_type='application/json')

def get_menus_for_this_role(request):
    role = request.session["user_info"][4]
    menus = Menus.objects.filter(roles__contains=role)
    return menus


def edit_profile(request):
    user_info = request.session.get('user_info')
    if user_info is not None:
        menus = get_menus_for_this_role(request)
        print({'menus': menus})
        context = {
            'activeLink': '',
            'menus': menus,
            'full_name': user_info[2] + ' ' + user_info[3],
            'role': user_info[4],
            'first_name': user_info[2],
            'last_name': user_info[3],
            'email': user_info[1],
            'user_id': user_info[0],
        }
        return render(request, 'profile.html', context)
    else:
        return HttpResponseRedirect('/')


def display_home_page(request):
    user_info = request.session.get('user_info')
    if user_info is not None:
        menus = get_menus_for_this_role(request)
        print({'menus': menus})
        context = {
            'activeLink': 'Home',
            'menus': menus,
            'full_name': user_info[2] + ' ' + user_info[3],
            'role': user_info[4]
        }
        return render(request, 'home.html', context)
    else:
        return HttpResponseRedirect('/')


def display_customers_page(request):
    user_info = request.session.get('user_info')
    if user_info is not None:
        menus = get_menus_for_this_role(request)
        context = {
            'activeLink': 'Customers',
            'menus': menus,
            'full_name': user_info[2] + ' ' + user_info[3],
            'role': user_info[4],
            'customers': get_customers()
        }
        return render(request, 'customers.html', context)
    else:
        return HttpResponseRedirect('/')


def display_users_page(request):
    user_info = request.session.get('user_info')
    if user_info is not None:
        menus = get_menus_for_this_role(request)
        context = {
            'activeLink': 'Users',
            'menus': menus,
            'full_name': user_info[2] + ' ' + user_info[3],
            'role': user_info[4]
        }
        return render(request, 'users.html', context)
    else:
        return HttpResponseRedirect('/')


def display_orders_page(request):
    user_info = request.session.get('user_info')
    if user_info is not None:
        menus = get_menus_for_this_role(request)
        context = {
            'activeLink': 'Orders',
            'menus': menus,
            'full_name': user_info[2] + ' ' + user_info[3],
            'role': user_info[4]
        }
        return render(request, 'orders.html', context)
    else:
        return HttpResponseRedirect('/')


def get_order_by_id(request):
    if request.method == 'POST':
        order = serializers.serialize('json', Order.objects.filter(order_no=request.POST['order_no']))
        return HttpResponse(order, content_type='application/json')
