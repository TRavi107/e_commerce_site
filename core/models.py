from django.db import models
from django.shortcuts import reverse 
from django.conf import settings

# Create your models here.
CATEGORIES_CHOICES = (
    ('S','Shirt'),
    ('SW','Sport wear'),
    ('OW','Out wear'),

)

LABEL_CHOICES = (
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),

)

class Items(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='items_img/')
    categories= models.CharField(choices=CATEGORIES_CHOICES,max_length=2)
    label= models.CharField(choices=LABEL_CHOICES,max_length=1,blank=True,null=True)
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True,blank=True)
    description = models.CharField(max_length=1000,null=True,blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_abs_url(self):
        return reverse("core:product",kwargs={
            'slug':self.slug
        })

    def get_add_to_card_url(self):
        return reverse("core:add_to_cart",kwargs={
            'slug':self.slug,
        })

    def get_remove_from_card_url(self):
        return reverse("core:remove_from_cart",kwargs={
            'slug':self.slug
        })

class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,blank=True,null=True)
    contents = models.CharField(max_length=1000)
    item = models.ForeignKey(Items,on_delete=models.CASCADE)
    posted_time = models.TimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.contents

    #This need to be finished
    def get_posted_time(self):
        pass


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    item = models.ForeignKey(Items,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered= models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_add_to_card_url(self):
        return reverse("core:add_to_cart_c",kwargs={
            'slug':self.item.slug,
        })

    def get_remove_from_card_url(self):
        return reverse("core:remove_from_cart_c",kwargs={
            'slug':self.item.slug
        })

    def get_remove_from_card_all_url(self):
        return reverse("core:remove_from_cart_all",kwargs={
            'slug':self.item.slug
        })

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)

    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered= models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'BillingAddress',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)

    street_address = models.CharField(max_length=100)
    apartment_address =models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    
