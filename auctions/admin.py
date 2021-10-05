from typing import List
from django.contrib import admin

from .models import Bid, Category, Comment, Listing
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'photo', 'price', 'description')

class CategoryAdmin(admin.ModelAdmin):
    pass

class BidAdmin(admin.ModelAdmin):
    pass


admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)