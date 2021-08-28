from django.urls import path
from App_Payment import views

app_name='App_Payment'

urlpatterns=[
    path('checkout/', views.checkout,name="checkout"),
    path('complete/',views.complete,name="complete"),
    path('pay/',views.payment,name="payment"),
    path('order/',views.order_view,name="order"),
    path('purchase/<val_id>/<tran_id>/',views.purchase, name="purchase"),
    path('review_order/<pk>/',views.review_order,name="review_order"),
    path('rate_review/<pk>/<fk>/',views.rate_review,name="review"),
]
