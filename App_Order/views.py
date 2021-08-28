from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from App_Shop.models import Food
# Create your views here.
from App_Order.models import Order, Cart
from App_Review.models import Review,Review_Cart
from App_Review.forms import ReviewForm

@login_required
def add_to_cart(request, pk):
    item=get_object_or_404(Food, pk=pk)
    order_item=Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity +=1
            order_item[0].save()
            messages.info(request,"This item quantity is updated")
            return redirect('App_Shop:home')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to your cart")
            return redirect('App_Shop:home')
    else:
        order=Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, "This item was added")
        return redirect('App_Shop:home')
@login_required
def cart_view(request):
    carts=Cart.objects.filter(user=request.user, purchased=False)
    orders=Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order=orders[0]
        return render(request, 'App_Order/cart.html',context={'carts':carts, 'order':order})
    else:
        messages.warning(request, "You don't have any item in your cart")
        return redirect('App_Shop:home')
@login_required
def increase_quantity(request,pk):
    item=get_object_or_404(Food, pk=pk)
    order_item=Cart.objects.get_or_create(item=item,user=request.user, purchased=False)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_item[0]
        if order.quantity >=1:
                order.quantity +=1
                order.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect('App_Order:cart_view')
        else:
            messages.info(request,"This item doesnot exist in your Order")
            return redirect('App_Order:cart_view')
    else:
        messages.info(request,"This item quantity is not in your order list")
        return redirect('App_Order:cart_view')
@login_required
def decrease_quantity(request,pk):
    item=get_object_or_404(Food, pk=pk)
    order_item=Cart.objects.get_or_create(item=item,user=request.user, purchased=False)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_item[0]
        if order.quantity >1:
                order.quantity -=1
                order.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect('App_Order:cart_view')
        else:
            messages.info(request,"Can't decrease to 0, Please Click the Remove button")
            return redirect('App_Order:cart_view')
    else:
        messages.info(request,"This item quantity is not in your order list")
        return redirect('App_Order:cart_view')
@login_required
def remove_from_cart(request,pk):
    item=get_object_or_404(Food, pk=pk)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item=Cart.objects.get_or_create(item=item,user=request.user, purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was removed from your Cart")
            return redirect('App_Order:cart_view')
        else:
            messages.info(request, "This item is not in your Cart")
            return redirect('App_Shop:home')
    else:
        messages.info(request, "This item is not in your Ordered List")
        return redirect('App_Shop:home')

@login_required
def order_review(request,pk, r_pk):
    order=Order.objects.get(pk=pk, ordered=True)
    return render(request, "App_Order/order_review.html",context={'order':order})
@login_required
def feedback(request,pk):
    order=Order.objects.get(pk=pk, ordered=True)
    review=Review.objects.get(user=request.user,order=order, reviewed=False)
    print(review.pk)
    form=ReviewForm(instance=review)
    if request.method =='POST':
        form=ReviewForm(request.POST,instance=review)
        if form.is_valid():
            form.save(commit=False)
            review.user=request.user
            review.reviewed=True
            order.order_done=True
            order.save()
            review.save()
            form.save(commit=True)
            form=ReviewForm(instance=review)
            messages.success(request, "Thank You For Your Kind Feedback")
            return redirect('App_Shop:home')
    return render(request, "App_Order/feedback.html",context={'form':form})
