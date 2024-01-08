from django import forms
from .constants import REVIEW_TYPE


class BorrowBookForm(forms.Form):
    book_id=forms.IntegerField()

class ReturnBookForm(forms.Form):
    borrow_id=forms.IntegerField()


    

    
class ReviewBookForm(forms.Form):
    review = forms.ChoiceField(
        choices=REVIEW_TYPE,
        label="Choose Review",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )