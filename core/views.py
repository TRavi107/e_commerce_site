from django.shortcuts import render,get_object_or_404,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView,DetailView,View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import (
    Items,
    OrderItem,
    Order,
    BillingAddress,
    Comments
)
from django.utils import timezone
from django.contrib import messages
from .forms import Checkoutform,CommentForm
from .filter import ItemsFilter
# Create your views here.


class  HomeView(ListView):
    paginate_by = 4
    template_name = "home-page.html"
    model = Items

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ItemsFilter(self.request.GET,queryset=self.get_queryset())
        return context

def filter_by_categories(request,categories):
    items = Items.objects.all()
    queryset = items.filter(categories=categories)
    filter = ItemsFilter(request.GET,queryset=queryset)
    context = {
        'queryset':queryset,
        'filter':filter
    }
    return render(request,"home-page.html",context=context)

class  ItemDetailView(DetailView):
    model = Items
    template_name = "product-page.html"

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        comments =Comments.objects.all().filter(item = self.get_object())
        context['comments'] = comments
        return context

    def post(self,*args,**kwargs):
        if 'ReplyForm' in self.request.POST:
            parent_id = self.request.POST.get('parent_id')

        else :
            parent_id=None

        form = CommentForm(self.request.POST or None)

        if form.is_valid() :
            item = self.get_object()
            contents = form.cleaned_data.get("contents")
            if self.request.user.is_authenticated:
                user = self.request.user
            else:
                user = None
            comment = Comments(
                user=user,
                contents=contents,
                item = item,
                parent_id = parent_id
            )
            comment.save()
            return redirect(".")

        messages.info(self.request,"Form or item is invalid")
        return redirect(".")


class CheckOutView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            form = Checkoutform()
            context = {
                'object':order,
                'form':form
            }
            return render(self.request,'checkout-page.html',context)

        except ObjectDoesNotExist:
            messages(self.request,"You do not have active order")
            return redirect("/")

    def post(self,*args,**kwargs):
        form = Checkoutform(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)

            if form.is_valid():
                street_address= form.cleaned_data.get('street_address')
                apartment_address= form.cleaned_data.get('apartment_address')
                zip= form.cleaned_data.get('zip')
                same_billing_address= form.cleaned_data.get('same_billing_address')
                save_info= form.cleaned_data.get('save_info')
                payment_option= form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    zip= zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                return redirect('core:CheckOutView')

            messages.info(self.request,"Failed checkout")
            return redirect("core:CheckOutView")

        except ObjectDoesNotExist:
            messages(self.request,"You do not have active order")
            return redirect("/")
        
        #return redirect("core:CheckOutView")

class PaymentView(View):
    def get(self,*args,**kwargs):
        return render (self.request,"payment.html")

@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Items,slug=slug)
    order_item ,created = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False    
    )
    order_qs = Order.objects.filter(user=request.user,ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            messages.info(request,"This item quantity was updated")
            order_item.quantity +=1
            order_item.save()
            return redirect("core:product",slug = slug)

        else:
            messages.info(request,"This item was added")
            order_item.quantity=1
            order_item.save()
            order.items.add(order_item)
            return redirect("core:product",slug = slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user,ordered_date=ordered_date)
        messages.info(request,"This item was added")
        order_item.save()
        order.items.add(order_item)
        return redirect("core:product",slug = slug)

@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Items,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user = request.user,
                ordered = False    
            )[0]
            messages.info(request,"This item was removed")
            order.items.remove(order_item)
            return redirect("core:product",slug = slug)

        else:
            messages.info(request,"you dont have this item on cart")
            return redirect("core:product",slug = slug)

    else:
        messages.info(request,"You have no active order")
        return redirect("core:product",slug = slug)
        
    return redirect("core:product",slug = slug)

@login_required
def remove_from_cart_all(request,slug):
    item = get_object_or_404(Items,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user = request.user,
                ordered = False    
            )[0]
            messages.info(request,"This item was removed")
            order.items.remove(order_item)
            return redirect("core:CheckOutView")

        else:
            messages.info(request,"you dont have this item on cart")
            return redirect("core:CheckOutView")

    else:
        messages.info(request,"You have no active order")
        return redirect("core:CheckOutView")
        
    return redirect("core:CheckOutView")


@login_required
def add_to_cart_c(request,slug):
    item = get_object_or_404(Items,slug=slug)
    order_item ,created = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False    
    )
    order_qs = Order.objects.filter(user=request.user,ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            messages.info(request,"This item quantity was updated")
            order_item.quantity +=1
            order_item.save()
            return redirect("core:CheckOutView")

        else:
            messages.info(request,"This item was added")
            order_item.quantity=1
            order_item.save()
            order.items.add(order_item)
            return redirect("core:CheckOutView")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user,ordered_date=ordered_date)
        messages.info(request,"This item was added")
        order_item.save()
        order.items.add(order_item)
        return redirect("core:CheckOutView")

def like_the_comment(request,id):
    comment = get_object_or_404(Comments,id=id)
    if comment != None:
        comment.likes +=1
        comment.save()
        comm ={
            'contents':comment.contents,
            'username':comment.user.username,
            'likes':comment.likes,
            'parent':comment.parent_id
        }
        data ={
            'data':comm
        }

    return JsonResponse(data)

def dislike_the_comment(request,id):
    comment = get_object_or_404(Comments,id=id)
    if comment != None:
        comment.dislikes +=1
        comment.save()
        comm ={
            'contents':comment.contents,
            'username':comment.user.username,
            'dislikes':comment.dislikes,
            'parent':comment.parent_id
        }
        data ={
            'data':comm
        }

    return JsonResponse(data)

@login_required
def remove_from_cart_c(request,slug):
    item = get_object_or_404(Items,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user = request.user,
                ordered = False    
            )[0]
            if(order_item.quantity >1):
                order_item.quantity -=1
                order_item.save()

            else:
                messages.info(request,"This item was removed")
                order.items.remove(order_item)
            return redirect("core:CheckOutView")

        else:
            messages.info(request,"you dont have this item on cart")
            return redirect("core:CheckOutView")

    else:
        messages.info(request,"You have no active order")
        return redirect("core:CheckOutView")
        
    return redirect("core:CheckOutView")