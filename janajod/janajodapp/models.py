from django.db import models
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    media = models.FileField(upload_to='post_media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional: Add likes, dislikes, etc.
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at}'
    


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.id}'



from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)  # Add this line

    def __str__(self):
        return self.title



# models.py
from django.db import models
from django.contrib.auth.models import User

class UserEventRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Track approval status

    def __str__(self):
        return self.title



from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link complaint to user
    fullname = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)  # Optional field
    location = models.CharField(max_length=255)
    complaint = models.TextField()
    image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)  # Optional field
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when complaint is created

    def __str__(self):
        return f"Complaint by {self.fullname} - {self.location}"



from django.db import models
from django.contrib.auth.models import User

class ServiceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link service request to user
    fullname = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    
    email = models.EmailField(blank=True, null=True)  # Optional field
    service_type = models.CharField(max_length=255)  # New field for service type
    description = models.TextField()  # Details about the service request
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)  # Optional field for images
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when service request is created

    def __str__(self):
        return f"Service Request by {self.fullname} - {self.service_type}"



class Job(models.Model):
    organization = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return f"{self.job_title} at {self.organization}"




class UserReqJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)  # This is your timestamp field
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.job_title} at {self.organization}"


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)
    user_job = models.ForeignKey(UserReqJob, on_delete=models.CASCADE, related_name='user_applications', null=True, blank=True)
    applicant_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    why_this_job = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 

    def __str__(self):
        if self.job:
            return f"Application by {self.applicant_name} for {self.job.job_title}"
        else:
            return f"Application by {self.applicant_name} for {self.user_job.job_title}"



from django.db import models

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
     return f"Feedback from {self.user.username}"


# models.py
from django.db import models

from django.db import models

class Survey(models.Model):
  title = models.CharField(max_length=255)
  posted_on = models.DateTimeField(auto_now_add=True)
   

class Question(models.Model):
  survey = models.ForeignKey(Survey, on_delete=models.CASCADE)  # Foreign key to Survey model
  text = models.TextField()

class Option(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Foreign key to Question model
  text = models.CharField(max_length=255)
  
  
class SurveyResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.user.username} for {self.survey.title}"
    
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
    
    
    
    
from django.db import models

class CommitteeMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    contribution = models.TextField()
    profile_picture = models.ImageField(upload_to='images/users/', null=True, blank=True)

    def __str__(self):
        return self.name



