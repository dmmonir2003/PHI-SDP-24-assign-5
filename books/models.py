
from django.db import models
from .constants import REVIEW_TYPE
from django.contrib.auth.models import User

    

class Categories(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    

class Book(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='books')
    aurthor_name=models.CharField(max_length=100,blank=True,null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    borrowing_price = models.IntegerField(default=0)
    user_reviews = models.IntegerField(choices=REVIEW_TYPE, null=True,blank=True)
    image_url = models.URLField() 
    is_available = models.BooleanField(default=False,blank=True,null=True) 

    def __str__(self):
        return self.title

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowing_date = models.DateField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    returned_date = models.DateField(null=True)

    def __str__(self):
        return f'user-name{self.user.first_name}-book {self.book.title}'
    


    
