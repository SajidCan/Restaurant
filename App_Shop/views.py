from django.shortcuts import render
from django.views.generic import ListView,DetailView
from App_Shop.models import Food, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from App_Review.models import Review,Review_Cart
from App_Order.models import Order
from App_Login.models import Profile
# Create your views here.

# class Home(ListView):
#     model=Food
#     template_name='App_Shop/home.html'


def home(request):
    if request.user.is_authenticated:
        review=Review.objects.filter(user=request.user, reviewed=False)
        order_cart=Order.objects.filter(user=request.user, ordered=True)
        foods=Food.objects.filter(fav=True)
        categories=Category.objects.all()
        reviews=Review_Cart.objects.filter(reviewed_food=True, admin_check=True)
        return render(request,'App_Shop/home.html',context={'foods':foods,'categories':categories,'reviews':reviews,'review':review, 'order_cart':order_cart})
    else:
        foods=Food.objects.filter(fav=True)
        categories=Category.objects.all()
        reviews=Review_Cart.objects.filter(reviewed_food=True, admin_check=True)
        return render(request,'App_Shop/home.html',context={'foods':foods,'categories':categories,'reviews':reviews})
def food_details(request,pk):
    review_exists=False
    food=Food.objects.get(pk=pk)
    reviews=Review_Cart.objects.filter(item=food, reviewed_food=True, admin_check=True)
    print(reviews)
    if reviews:
        review_exists=True
    # profile=Profile.objects.get(user=reviewed_user)
    # user_reviewed=profile.username
    # review_text=review.review_food
    # if(review):
    #     review_exists=True

    return render(request,'App_Shop/food_details.html',context={'food':food,'review_exists':review_exists,'reviews':reviews})
def category_food(request,pk):
    categories=Category.objects.get(pk=pk)
    foods=Food.objects.filter(category=categories)
    return render(request,'App_Shop/category_foods.html',context={'foods':foods,'categories':categories})
