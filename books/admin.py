from django.contrib import admin
from .models import Categories,Book,BorrowedBook

# Register your models here.
admin.site.register(Categories)
admin.site.register(Book)
admin.site.register(BorrowedBook)