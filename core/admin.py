from django.contrib import admin
from .models import Items,Order,OrderItem,Comments
# Register your models here.

admin.site.register(Items)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Comments)


