from django.urls import path
from App_Shop import views

app_name='App_Shop'

urlpatterns=[
    path('',views.home, name="home"),
    path('food/<pk>/',views.food_details, name="food_details",),
    path('category/<pk>/',views.category_food,name="category_food"),
]
