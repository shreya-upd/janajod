from django.forms import forms
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))

    last_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))

    username = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))

    email = forms.EmailField(max_length=200, widget=forms.EmailInput(
        attrs={'class':'form-control'
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control'}
    ))
    

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control'}
    ))
    

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
        
# janajodapp/forms.py

from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['profile_image', 'full_name', 'contact_number', 'address', 'bio']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['full_name'].initial = self.instance.full_name
            self.fields['contact_number'].initial = self.instance.contact_number
            self.fields['address'].initial = self.instance.address
            self.fields['bio'].initial = self.instance.bio

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile



# janajodapp/forms.py

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': "What's on your mind?",
            'class': 'form-control',
            'rows': 3
        }),
        max_length=500,
        required=True
    )
    media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'accept': 'image/*, video/*'
        })
    )

    class Meta:
        model = Post
        fields = ['content', 'media']


# janajodapp/forms.py

from django import forms
from .models import Post, Comment
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Post a comment',
            'class': 'form-control',
        }),
        max_length=300,
        required=True
    )

    class Meta:
        model = Comment
        fields = ['content']


from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'media']  # Ensure these are the fields you want to allow editing


from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['fullname', 'contact', 'email', 'location', 'complaint', 'image']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your full name'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your contact number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter your email address'}),
            'location': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your location including tole,ward..'}),
            'complaint': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Describe your complaint'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


from django import forms
from .models import ServiceRequest

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['fullname', 'contact', 'email', 'service_type', 'description', 'location','image']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your contact number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
            'service_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the type of service required'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your service request'}),
            'location': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your location including tole,ward..'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }




