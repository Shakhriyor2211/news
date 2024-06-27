from django import forms


from news_app.models import Contact, News, Comments


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"




class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['body']
