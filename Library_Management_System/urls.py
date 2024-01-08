
from django.contrib import admin
from django.urls import path,include
from core.views import BookListView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',BookListView.as_view(),name='homepage'),
    path('profiles/',include('profiles.urls')),
    path('book/',include('books.urls')),
]
