from django.urls import path
from App_Order import views

app_name='App_Order'

urlpatterns=[
     path('add_to_cart/<pk>/',views.add_to_cart, name="add_to_cart"),
     path('cart/',views.cart_view,name="cart_view"),
     path('order_review/<pk>/<r_pk>/',views.order_review,name="order_review"),
     path('feedback/<pk>/',views.feedback,name="feedback"),
     path('increase_quantity/<pk>/',views.increase_quantity, name="increase_quantity"),
     path('decrease_quantity/<pk>/',views.decrease_quantity, name="decrease_quantity"),
     path('remove_from_cart/<pk>/',views.remove_from_cart,name="remove_from_cart"),
]
