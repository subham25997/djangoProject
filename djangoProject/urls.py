from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_login, name='login'),
    path('logout', views.logout, name='logout'),
    path('login-page', views.login, name='login'),
    path('register', views.register, name='register'),
    path('save-user', views.save_user, name='save_user'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('validate-login/', views.validate_login, name='validate_login'),
    path('home/', views.display_home_page, name='display_home_page'),
    path('users/', views.display_users_page, name='display_users_page'),
    path('customers/', views.display_customers_page, name='display_customers_page'),
    path('get_all_customers/', views.get_all_customers, name='get_all_customers'),
    path('customers-by-id/', views.get_customer_by_id, name='get_customer_by_id'),
    path('save-customer', views.save_customer, name='save_customer'),
    path('orders/', views.display_orders_page, name='display_orders_page'),
    path('get_all_products/', views.get_all_products, name='get_all_products'),
    path('create-order/', views.create_order, name='create_order'),
    path('get_all_orders/', views.get_all_orders, name='get_all_orders'),
    path('order-by-id/', views.get_order_by_id, name='get_order_by_id'),
]
