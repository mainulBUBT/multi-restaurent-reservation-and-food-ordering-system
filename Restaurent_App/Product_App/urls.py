from django.urls import path

from Product_App import views

app_name = 'Product_App'

urlpatterns = [
    path('', views.index, name='index'),
    path('reservation/<int:id>', views.reservation, name='reservation'),
    path('ur_reserve/', views.ur_reserve, name='ur_reserve'),
    path('menus/<int:id>', views.menu_list, name='menus'),
    path('orders/<tran_id>/<method>/<service_type>/<rest_id>', views.orders, name='orders'),
    path('pdf/<int:id>', views.generate_pdf, name='pdf'),
    path('payments/', views.payments, name='payments'),
    path('billing/', views.bill, name='bill'),
    path('check_cart/<int:id>', views.check_cart, name='check_cart'),
    path('histories/', views.histories, name='histories'),
    path('checkout/', views.checkout, name='checkout'),
    path('test/<int:id>', views.test, name='test'),


    # Cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/<int:id>', views.cart_detail, name='cart_detail'),
]
