from django import forms

class SearchForm(forms.Form):
    CATEGORY_CHOICES = ( ('ALL', 'All'),
                         ('APPLICATIONS', 'Applications'),
                         ('AUDIO', 'Audio'),
                         ('GAMES', 'Games'),
                         ('VIDEO', 'Video'),
                         ('OTHER', 'Other') )
    search_string = forms.CharField(max_length=50)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)