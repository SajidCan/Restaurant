from django.shortcuts import render,redirect, HttpResponseRedirect, get_object_or_404
from App_Payment.forms import BillingForm
from App_Order.models import Order, Cart
from App_Shop.models import Food
from App_Review.models import Review,Review_Cart
from App_Review.forms import ReviewRateForm
from App_Payment.models import BillingAddress
from django.contrib import messages
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import socket
import time
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    saved_address=BillingAddress.objects.get_or_create(user=request.user)[0]
    form=BillingForm(instance=saved_address)
    if request.method == 'POST':
        form=BillingForm(request.POST,instance=saved_address)
        if form.is_valid():
            form.save()
            form=BillingForm(instance=saved_address)
            messages.success(request,"Shipping Address Saved")
    order_qs=Order.objects.filter(user=request.user, ordered=False)[0]
    order=order_qs.orderitems.all()
    order_total=order_qs.get_totals()
    return render(request,'App_Payment/checkout.html',context={'form':form,'order':order,'order_total':order_total,'saved_address':saved_address})

@login_required
def payment(request):
    saved_address=BillingAddress.objects.get_or_create(user=request.user)[0]
    if not saved_address.is_fully_filled():
        messages.info(request,"Please fill up the Billing Information Form")
        return redirect('App_Payment:checkout')
    elif not request.user.profile.is_fully_filled():
        messages.info(request, "Please fill up Your Profile Information")
        return redirect('App_Login:user_profile')
    store_id='resta6106cc1632258'
    api='resta6106cc1632258@ssl'
    status_url=request.build_absolute_uri(reverse('App_Payment:complete'))
    order_qs=Order.objects.filter(user=request.user, ordered=False)[0]
    order=order_qs.orderitems.all()
    order_count=order_qs.orderitems.count()
    order_totals=order_qs.get_totals()
    current_user=request.user
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=api)
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)
    mypayment.set_product_integration(total_amount=Decimal(order_totals), currency='BDT', product_category='Mixed', product_name=order, num_of_item=order_count, shipping_method='Courier', product_profile='None')
    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, address1=current_user.profile.address_1, address2=current_user.profile.address_1, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)
    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=saved_address.address, city=saved_address.city, postcode=saved_address.zipcode, country=saved_address.country)
    response_data = mypayment.init_payment()
    print(response_data)
    return redirect(response_data['GatewayPageURL'])
@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method =='post':
        payment_data=request.POST
        status=payment_data['status']
        if status == 'VALID':
            val_id= payment_data['val_id']
            tran_id= payment_data['tran_id']
            messages.success(request, "Your Payment Completed Successfully")
            return HttpResponseRedirect(reverse('App_Payment:purchase', kwargs={'val_id':val_id,'tran_id':tran_id}))
        elif status == 'FAILED':
            messages.warning(request, "Your Payment Failed to Complete, Try Again")
    return render(request, 'App_Payment/complete.html',context={})
@login_required
def purchase(request, val_id, tran_id):
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    order=order_qs[0]
    orderId=tran_id
    order.ordered = True
    order.orderId=orderId
    order.paymentId=val_id
    order.order_to_review=order.orderitems.count()
    order.save()
    cart_items=Cart.objects.filter(user=request.user,  purchased=False)
    for item in cart_items:
        item.purchased=True
        item.save()

    review_order=Review(order=order,user=request.user, reviewed=False)
    review_order.save()
    for x in order.orderitems.all():
        y=str(x.get_orders())
        # print(y)
        item=get_object_or_404(Food, name=y)
        # print(item)
        rev_food=Review_Cart.objects.get_or_create(item=item, user=request.user, reviewed_food=False)
        print(rev_food)
        # food=Food.objects.filter(name=y)
        rev=rev_food[0]
        review_order.orderitems.add(rev)
        review_order.save()
    return HttpResponseRedirect(reverse('App_Shop:home'))
@login_required
def order_view(request):
    try:
        orders=Order.objects.filter(user=request.user, ordered=True)

        context={"orders":orders}
    except:
        messages.warning(request,"You do not have any active order")
        return redirect("App_Shop:home")
    return render(request, "App_Payment/order.html",context)
@login_required
def review_order(request,pk):
    ordered_food=Order.objects.get(pk=pk)
    fk=pk
    # review_order=Review.objects.get_or_create(order=ordered_food,user=request.user, reviewed=False)
    # for x in ordered_food.orderitems.all():
    #     y=str(x.get_orders())
    #     # print(y)
    #     item=get_object_or_404(Food, name=y)
    #     # print(item)
    #     rev_food=Review_Cart.objects.get_or_create(item=item, user=request.user, reviewed_food=False)
    #     # food=Food.objects.filter(name=y)
    #     if review_order.exists():
    #         review=review_order[0]
    #         if not review.orderitems.filter(item=item).exists():
    #             review.orderitems.add(rev_food[0])
    #             review.save()
    #         else:
    #             review=Review_Cart(user=request.user, order=ordered_food, reviewed=False)
    #             review.orderitems.add(rev_food[0])
    #             review.save()
    # # print(reviews[0].item.name)
    # # review_left=ordered_food.order_to_review
    # # print(rev_food[0].item)
    # rev=Review.objects.filter(user=request.user, reviewed=False, order=ordered_food)[0]
    # print(rev.orderitems.all())
    rev=Review.objects.filter(user=request.user, reviewed=False, order=ordered_food)[0]
    print(rev.orderitems.all())
    return render(request, "App_Payment/review_order.html",context={"rev":rev,"fk":fk})

# def review_order(request,pk):
#     ordered_food=Order.objects.get(pk=pk)
#     print(ordered_food.orderitems)
#     reviews=Review.objects.filter(order=ordered_food,user=request.user, reviewed=False)
#     for x in ordered_food.orderitems.all():
#         y=str(x.get_orders())
#         print(y)
#         item=get_object_or_404(Food, name=y)
#         # food=Food.objects.filter(name=y)
#         if reviews.exists():
#             review=reviews[0]
#             review.item.add(food[0])
#             review.save()
#         else:
#             review=Review(user=request.user, order=ordered_food)
#             review.item.add(food[0])
#             review.save()
#     print(reviews[0].item.name)
#     review_left=ordered_food.order_to_review
#
#     return render(request, "App_Payment/review_order.html",context={'ordered_food':ordered_food,'review':review,'review_left':review_left})
@login_required
def rate_review(request, pk,fk):
    order_cart=Order.objects.filter(user=request.user, ordered=True)
    order=order_cart[0]
    pkk=fk
    food=Food.objects.get(pk=pk)
    order_qs=Review.objects.filter(user=request.user, reviewed=False)
    review=Review_Cart.objects.get(user=request.user, item=food,reviewed_food=False)
    if order_qs.exists():
        form=ReviewRateForm(instance=review)
        if request.method=='POST':
            form=ReviewRateForm(request.POST,instance=review)
            if form.is_valid():
                form.save(commit=False)
                review.user=request.user
                review.item=food
                review.reviewed_food=True
                order.order_to_review -=1
                order.save()
                review.save()
                form=ReviewRateForm(instance=review)
                return HttpResponseRedirect(reverse('App_Payment:order'))

    return render(request, "App_Payment/rate_review.html",context={'form':form})
