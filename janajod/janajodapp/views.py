from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib import messages

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode


# janajodapp/views.py

from django.shortcuts import render, redirect

from .forms import ProfileUpdateForm, PostForm
from django.contrib import messages
from .models import Post

# views.py in your app
from django.shortcuts import render
from .models import Profile  # Import any model you want to display
from django.contrib.auth.decorators import login_required

@login_required
def custom_admin_home(request):
    users = Profile.objects.all()  # Query some data, like all profiles
    return render(request, 'custom_admin_home.html', {'users': users})

from django.contrib.auth.models import User

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import UserEditForm

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect to the user list page after saving
    else:
        form = UserEditForm(instance=user)
    return render(request, 'edit_user.html', {'form': form, 'user': user})


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'delete_user_confirm.html', {'user': user})

# views.py
from django.shortcuts import render, redirect
from .forms import UserCreateForm

def add_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect back to the user list page after saving
    else:
        form = UserCreateForm()
    return render(request, 'add_user.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from .models import CommitteeMember
from .forms import CommitteeMemberForm

# View to list and add committee members
def committee_member_list(request):
    members = CommitteeMember.objects.all()
    form = CommitteeMemberForm()
    
    if request.method == 'POST':
        form = CommitteeMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('committee_members')
    
    context = {
        'members': members,
        'form': form,
    }
    return render(request, 'com-member.html', context)

# View to edit a committee member
def edit_committee_member(request, pk):
    member = get_object_or_404(CommitteeMember, pk=pk)
    form = CommitteeMemberForm(request.POST or None, request.FILES or None, instance=member)
    
    if form.is_valid():
        form.save()
        return redirect('committee_members')
    
    return render(request, 'edit_committee_member.html', {'form': form, 'member': member})

# View to delete a committee member
def delete_committee_member(request, pk):
    member = get_object_or_404(CommitteeMember, pk=pk)
    
    if request.method == 'POST':
        member.delete()
        return redirect('committee_members')
    
    return render(request, 'delete_committe_member.html', {'member': member})

def admin_complain(request):
    complaints = Complaint.objects.all()
    return render(request, 'admincomplaints.html', {'complaints': complaints})

from django.shortcuts import render, redirect
from .forms import ComplaintForm  # Define this form in forms.py


def add_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)  # Create complaint instance without saving to the database yet
            complaint.user = request.user  # Assign the logged-in user to the complaint
            complaint.save()  # Now save the complaint with the user assigned
            return redirect('admin_complain')  # Redirect to the complaints list page
    else:
        form = ComplaintForm()
    return render(request, 'add_complaint.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Complaint

def show_complaint(request, complaint_id):
    # Get the complaint by ID
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    return render(request, 'show_complaint.html', {'complaint': complaint})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Complaint
from .forms import ComplaintForm

def edit_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('show_complaint', complaint_id=complaint.id)
    else:
        form = ComplaintForm(instance=complaint)

    return render(request, 'edit_complaint.html', {'form': form, 'complaint': complaint})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Complaint

def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == 'POST':
        complaint.delete()
        return redirect('admin_complain')

    return render(request, 'confirm_delete_complaint.html', {'complaint': complaint})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required

# List Events
@login_required
def admin_events(request):
    events = Event.objects.all().order_by('-created_at')  # Show newest events first
    return render(request, 'adminevent.html', {'events': events})

# Add Event
@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user  # Set the current user as the author
            event.save()
            return redirect('admin_events')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})

# Edit Event
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('admin_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'edit_event.html', {'form': form})

# Approve Event
@login_required
def approve_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.is_approved = True
    event.save()
    return redirect('admin_events')

# Confirm Delete Event
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        event.delete()
        return redirect('admin_events')  # Redirect to the events list after deletion
    return render(request, 'adminneventdelete.html', {'event': event})

from django.shortcuts import render
from .models import Feedback

def show_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')  # Fetch feedback in descending order
    return render(request, 'showfeedback.html', {'feedbacks': feedbacks})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Feedback

def delete_feedback(request, feedback_id):
    # Fetch the feedback by its ID
    feedback = get_object_or_404(Feedback, id=feedback_id)
    
    if request.method == 'POST':
        # Delete the feedback
        feedback.delete()
        # Redirect back to the feedback list
        return redirect('showfeedback')  # Replace 'feedback_list' with the appropriate view name

    # In case the request is not POST, render the feedback list with a confirmation form
    return render(request, 'showfeedback.html', {'feedbacks': Feedback.objects.all()})


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import JobApplication
from .forms import JobApplicationForm

def admin_job_applications(request):
    applications = JobApplication.objects.all()
    return render(request, 'adminjobappli.html', {'applications': applications})

# In your views.py
from django.shortcuts import render, redirect
from .models import JobApplication

from django.shortcuts import render, redirect
from .models import JobApplication
from .forms import JobApplicationForm

def add_job_application(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new job application
            return redirect('admin_job_applications')  # Redirect to the job applications list page
    else:
        form = JobApplicationForm()

    return render(request, 'addjobappli.html', {'form': form})


# Edit Job Application
from django.shortcuts import get_object_or_404, render, redirect
from .models import JobApplication
from .forms import JobApplicationForm  # Assuming you have a form for job applications

def edit_job_application(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()  # Save the updated application
            return redirect('admin_job_applications')  # Redirect back to the list of job applications
    else:
        form = JobApplicationForm(instance=application)  # Load the form with existing data
    
    return render(request, 'jobappliedit.html', {'form': form, 'application': application})

from django.shortcuts import get_object_or_404, render, redirect
from .models import JobApplication

def delete_job_application(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)

    if request.method == 'POST':
        # If the POST request is made (i.e., 'Delete' button is clicked), delete the application
        application.delete()
        return redirect('admin_job_applications')  # Redirect back to the list of applications

    # If it's a GET request, show the confirmation page
    return render(request, 'jobapplidel.html', {'application': application})


from django.shortcuts import render, redirect
from .forms import JobForm
from django.shortcuts import render, redirect
from .forms import JobForm
from .models import Job

# Admin Job Listing
def admin_job_list(request):
    jobs = Job.objects.all()  # Fetch all jobs from the database
    return render(request, 'admin_jobs.html', {'jobs': jobs})

# Admin Post Job
def admin_post_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_job_list')  # Redirect back to the job listing page
    else:
        form = JobForm()

    return render(request, 'adminpostjob.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobForm
from .models import Job

# Edit Job
def admin_edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('admin_job_list')
    else:
        form = JobForm(instance=job)
    return render(request, 'adminpostjob.html', {'form': form})

# Delete Job
def admin_delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        job.delete()
        return redirect('admin_job_list')
    return render(request, 'adminjob_delete.html', {'job': job})

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import UserReqJob



class UserReqJobListView(ListView):
    model = UserReqJob
    template_name = 'userreqjob.html'
    context_object_name = 'userreqjobs'

    # Optional: You can filter or order the jobs
    def get_queryset(self):
        return UserReqJob.objects.all().order_by('-posted_on')


class UserReqJobCreateView(CreateView):
    model = UserReqJob
    fields = ['organization', 'job_title', 'job_description', 'is_approved']
    template_name = 'userreqjob_form.html'
    success_url = reverse_lazy('admin:userreqjob_list')

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from .models import UserReqJob
from .forms import UserReqJobForm  # Ensure you have a form for this model

# Update View for editing the job
class UserReqJobUpdateView(UpdateView):
    model = UserReqJob
    form_class = UserReqJobForm  # Your form for UserReqJob
    template_name = 'userreqjob_update.html'  # The template for editing the job
    success_url = reverse_lazy('userreqjob_list')  # Redirect to the job list after saving

    def get_object(self):
        return get_object_or_404(UserReqJob, pk=self.kwargs['pk'])


# Delete View for deleting the job
class UserReqJobDeleteView(DeleteView):
    model = UserReqJob
    template_name = 'userreqjob_confirm_delete.html'  # The template for confirming deletion
    success_url = reverse_lazy('userreqjob_list')  # Redirect to the job list after deletion

from django.shortcuts import render, get_object_or_404, redirect
from .models import UserEventRequest
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserEventRequest
from .forms import UserEventRequestForm

# List view for UserEventRequest
# List view for UserEventRequest
def userreqevent_list(request):
    events = UserEventRequest.objects.all()
    return render(request, 'userreqevent.html', {'events': events})


# Edit view for UserEventRequest
def userreqevent_edit(request, pk):
    event = get_object_or_404(UserEventRequest, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        is_approved = request.POST.get('is_approved') == 'on'  # Convert checkbox to boolean

        # Update event fields
        event.title = title
        event.description = description
        event.image = image
        event.is_approved = is_approved
        event.save()
        
        messages.success(request, 'Event updated successfully!')
        return redirect('userreqevent_list')
    
    return render(request, 'userreqevent_edit.html', {'event': event})

# Delete view for UserEventRequest
def userreqevent_delete(request, pk):
    event = get_object_or_404(UserEventRequest, pk=pk)
    event.delete()
    messages.success(request, 'Event deleted successfully!')
    return redirect('userreqevent_list')




def userreqevent_add(request):
    if request.method == 'POST':
        form = UserEventRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userreqevent_list') 
    else:
        form = UserEventRequestForm()

    return render(request, 'userreqevent_add.html', {'form': form})

# views.py
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post  # Adjust based on your actual model
from django.contrib.auth.decorators import login_required

@login_required
def viewpostadmin(request):
    posts = Post.objects.all()  # Get all posts
    selected_post = None

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if post_id:
            selected_post = Post.objects.get(id=post_id)  # Get selected post

    return render(request, 'viewpostadmin.html', {
        'posts': posts,
        'selected_post': selected_post,
    })

@login_required
def adminedit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('viewpostadmin')  # Redirect to admin post list
    else:
        form = PostForm(instance=post)
    return render(request, 'admineditpost.html', {'form': form, 'post': post})

@login_required
def admin_delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        # If the user confirms deletion, delete the post and redirect
        post.delete()
        return redirect('viewpostadmin')  # Redirect to the post list page
    
    return render(request, 'adminpost_delete.html', {'post': post})

from django.shortcuts import render, redirect
from .models import Post, User

def admin_add_post(request):
    if request.method == "POST":
        author = User.objects.get(id=request.POST['author'])
        content = request.POST['content']
        media = request.FILES.get('media', None)
        likes = request.POST.getlist('likes')
        dislikes = request.POST.getlist('dislikes')

        post = Post.objects.create(author=author, content=content, media=media)
        post.likes.set(likes)
        post.dislikes.set(dislikes)
        post.save()
        
        return redirect('viewpostadmin')  # Adjust to your post management page URL name

    users = User.objects.all()
    return render(request, 'adminaddpost.html', {'users': users})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile  # Import your Profile model
from .forms import ProfileUpdateForm  # Create a form for editing profiles

def profilemanage(request):
    # List all profiles
    profiles = Profile.objects.all()
    
    if request.method == "POST":
        # Handle bulk delete action
        action = request.POST.get('action')
        selected_profiles = request.POST.getlist('selected_profiles')
        if action == 'delete' and selected_profiles:
            Profile.objects.filter(id__in=selected_profiles).delete()
            return redirect('profilemanage')
    
    return render(request, 'profilemanage.html', {'profiles': profiles})

def edit_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profilemanage')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})

from django.shortcuts import get_object_or_404, redirect, render
from .models import Profile

def confirm_delete_profile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    return render(request, 'profiledelete.html', {'profile': profile})

def delete_profile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    profile.delete()
    return redirect('profilemanage')

# def add_profile_admin(request):
#     if request.method == 'POST':
#         form = ProfileUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('profilemanage')  # Redirect to profile management page
#     else:
#         form = ProfileUpdateForm()
#     return render(request, 'addprofileadmin.html', {'form': form})
from django.shortcuts import render
from .models import ServiceRequest

def view_service_requests(request):
    service_requests = ServiceRequest.objects.all()  # Fetch all service requests
    return render(request, 'viewservicereq.html', {'service_requests': service_requests})

from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceRequest
from .forms import ServiceRequestForm

def view_service_request_detail(request, id):
    service_request = get_object_or_404(ServiceRequest, id=id)
    
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES, instance=service_request)
        if form.is_valid():
            form.save()
            return redirect('view_service_requests')
    else:
        form = ServiceRequestForm(instance=service_request)
    
    return render(request, 'service_request_detail.html', {'form': form, 'service_request': service_request})

from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceRequest

def confirm_delete_service_request(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    return render(request, 'servicereq_delete.html', {'service_request': service_request})

def delete_service_request(request, pk):
    if request.method == "POST":
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        service_request.delete()
        return redirect('view_service_requests')  # Redirect to the list view
    return redirect('view_service_requests') 

from django.shortcuts import render, redirect
from .forms import ServiceRequestForm
from django.contrib.auth.decorators import login_required

@login_required
def add_service_request(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user  # Associate with the logged-in user
            service_request.save()
            return redirect('view_service_requests')
    else:
        form = ServiceRequestForm()

    return render(request, 'addservicereq.html', {'form': form})







@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('home')  # Replace 'home' with your actual home view name
        else:
            messages.error(request, 'There was an error creating your post. Please try again.')
    else:
        form = PostForm()

    # Fetch all posts ordered by creation date (newest first)
    posts = Post.objects.all().order_by('-created_at')

    context = {
        'form': form,
        'posts': posts,
    }
    return render(request, 'newsfeed.html', context)

# Existing views remain unchanged
# janajodapp/views.py

from .forms import CommentForm
from .models import Comment

@login_required(login_url='/login/')
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
        else:
            messages.error(request, 'There was an error adding your comment.')
    return redirect('home')  # Replace 'home' with your actual home view name

from django.shortcuts import get_object_or_404, redirect
from .models import Post

from django.shortcuts import get_object_or_404, redirect
@login_required(login_url='/login/')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Unliking
    else:
        post.likes.add(request.user)  # Liking
    
    # Redirect to the referring page
    return redirect(request.META.get('HTTP_REFERER', 'default_url_if_none'))  # Use a default URL if no referrer is found

from django.shortcuts import get_object_or_404, redirect
@login_required(login_url='/login/')
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)  # Remove dislike
    else:
        post.dislikes.add(request.user)  # Add dislike
    
    # Redirect to the referring page or a specific URL
    return redirect(request.META.get('HTTP_REFERER', 'default_url_if_none'))  # Use default if no referrer


from django.shortcuts import render, redirect, get_object_or_404

from .models import Post
from .forms import PostForm

@login_required(login_url='/login/')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the appropriate view after saving
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})

# views.py
from django.shortcuts import redirect, get_object_or_404
from .models import Post
@login_required(login_url='/login/')
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('home')  # or wherever you'd like to redirect after deletion


def register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # for sending Email
            current_site = get_current_site(request)
            mail_subject = "For Activate Your Account !!!!"

            message = render_to_string('activate_email_message.html',{
                'user':form.cleaned_data['username'],
                'domain': current_site.domain,
                'token': default_token_generator.make_token(user),
                'uid': urlsafe_base64_encode(force_bytes(user.pk))
            })

            to_email = form.cleaned_data['email']
            email = EmailMessage(
                mail_subject,message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Account created Successfully!!!!, Please Check your mail for activate your account.')
            return redirect('login')
        else:
            messages.error(request, 'Account creation failed!!!!. Please check & try again>>.')
    return render(request, 'register.html',{
        'form':form
    })



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or expired.')
        return render(request, 'activation_unsuccessful.html')

# views.py
from django.shortcuts import render, redirect
from .models import UserEventRequest, Event


from django.shortcuts import render
from .models import Event

from django.shortcuts import render
from .models import UserEventRequest

from django.shortcuts import render
from .models import UserEventRequest, Event
from django.db.models import Q
@login_required(login_url='/login/')
def events(request):
    # Fetch approved events from both models
    user_event_requests = UserEventRequest.objects.filter(is_approved=True).order_by('-created_at')
    admin_events = Event.objects.filter(is_approved=True).order_by('-created_at')

    # Combine the querysets
    all_events = sorted(
        list(user_event_requests) + list(admin_events), 
        key=lambda x: x.created_at, 
        reverse=True
    )

    return render(request, 'events.html', {'events': all_events})



@login_required
def submit_event(request):
    if request.method == 'POST':
        title = request.POST['event_title']
        description = request.POST['event_description']
        image = request.FILES.get('event_image')

        # Create a new UserEventRequest object
        event_request = UserEventRequest.objects.create(
            user=request.user,
            title=title,
            description=description,
            image=image
        )
        
        return redirect('events')  # Redirect to the event list page
    return render(request, 'events.html')  # Replace with your template


def wardpost(request):
    
    return render(request, 'wardposts.html')

def dashboard(request):
    
    return render(request, 'admindashboard.html')


def announce(request):
    
    return render(request, 'announce.html')

# def servicerequest(request):
    
#     return render(request, 'servicerequest.html')

# def complain(request):
    
#     return render(request, 'complain.html')


from django.shortcuts import render, redirect
from django.contrib import messages  # Import messages
from .forms import ComplaintForm
from .models import Complaint  
def complain(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user  # Assuming you want to save the user
            complaint.save()
            messages.success(request, "Your complaint has been submitted successfully!")  # Set success message
            return redirect('complain')  # Redirect to avoid form resubmission
    else:
        form = ComplaintForm()
        
        # Fetch the user's complaints to display them in the modal
    user_complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'complain.html', {'form': form, 'user_complaints': user_complaints}) 


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ServiceRequestForm
from .models import ServiceRequest

def servicerequest(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user  # Save the current user
            service_request.save()
            messages.success(request, "Your service request has been submitted successfully!")
            return redirect('servicerequest')  # Redirect to avoid form resubmission
    else:
        form = ServiceRequestForm()
    
    # Fetch the user's service requests to display them in the modal
    user_service_requests = ServiceRequest.objects.filter(user=request.user)
    return render(request, 'servicerequest.html', {'form': form, 'user_service_requests': user_service_requests})



# janajodapp/views.py

from django.shortcuts import render, redirect

from .forms import ProfileUpdateForm
from django.contrib import messages

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect to avoid form resubmission
        else:
            messages.error(request, 'Failed to update your profile. Please check the form for errors.')
    else:
        form = ProfileUpdateForm(instance=request.user.profile, user=request.user)

    return render(request, 'profile.html', {'form': form})



from django.shortcuts import render, redirect
from .models import Job, JobApplication


from django.shortcuts import render
from .models import Job, UserReqJob


from django.shortcuts import render
from .models import Job, JobApplication, UserReqJob
def job_listings(request):
    # Fetch all jobs (both admin and user-announced jobs)
    jobs = Job.objects.all().order_by('-posted_on')
    
    # Fetch applied jobs for the logged-in user
    applied_jobs = JobApplication.objects.filter(user=request.user).exclude(job_id__isnull=True, user_job_id__isnull=True)
    
    # Get the job_ids and user_job_ids into a list of tuples for easy lookup
    applied_jobs = applied_jobs.values_list('job_id', 'user_job_id')
    applied_jobs = list(applied_jobs)

    # Fetch approved UserReqJob entries (user-announced jobs)
    approved_user_req_jobs = UserReqJob.objects.filter(is_approved=True).order_by('-posted_on')
    
    # Admin posted jobs (Job model)
    admin_posted_jobs = Job.objects.all().order_by('-posted_on')

    return render(request, 'announce.html', {
        'jobs': jobs,
        'applied_jobs': applied_jobs,
        'admin_posted_jobs': admin_posted_jobs,
        'approved_user_req_jobs': approved_user_req_jobs
    })



from django.http import Http404
from .models import Job, UserReqJob, JobApplication

@login_required
@login_required
def apply_for_job(request, job_id):
    # Try to get the job from both Job and UserReqJob models
    try:
        # First try to get a Job (admin posted)
        job = Job.objects.get(id=job_id)
        user_job = None  # Not applicable in this case
    except Job.DoesNotExist:
        # If Job doesn't exist, try to get a UserReqJob (user posted job)
        user_job = UserReqJob.objects.get(id=job_id)
        job = None  # Not applicable in this case
    
    if request.method == 'POST':
        applicant_name = request.POST['fullname']
        contact_number = request.POST['contactNumber']
        address = request.POST['address']
        email = request.POST['email']
        why_this_job = request.POST['whyThisJob']

        # Create a new job application, either for a job or a user job
        if job:  # If it's a Job (admin job)
            JobApplication.objects.create(
                job=job,
                applicant_name=applicant_name,
                contact_number=contact_number,
                address=address,
                email=email,
                why_this_job=why_this_job,
                user=request.user  # Associate the application with the current user
            )
        elif user_job:  # If it's a UserReqJob (user job)
            JobApplication.objects.create(
                user_job=user_job,
                applicant_name=applicant_name,
                contact_number=contact_number,
                address=address,
                email=email,
                why_this_job=why_this_job,
                user=request.user  # Associate the application with the current user
            )

        # Redirect or render a success message
        return redirect('announce')

    # Return the appropriate job in the context, whether it's an admin job or a user-announced job
    return render(request, 'announce', {'job': job if job else user_job})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserReqJob
from django.views.decorators.http import require_POST

@require_POST
def create_announcement(request):
    if request.method == "POST":
        organization = request.POST.get('organization')
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')

        # Save the job announcement
        UserReqJob.objects.create(
            user=request.user,  # Set the user who created the announcement
            organization=organization,
            job_title=job_title,
            job_description=job_description,
        )

        messages.success(request, 'Announcement created successfully.')
        return redirect('announce')  # Redirect to a success page or the same page
    else:
        return render(request, 'announce.html')  # Replace with your template

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserReqJob, JobApplication

@login_required
def user_job_applications_view(request):
    # Get jobs posted by the logged-in user
    user_jobs = UserReqJob.objects.filter(user=request.user)
    # Filter applications for these jobs
    applications = JobApplication.objects.filter(user_job__in=user_jobs)
    
    return render(request, 'user_job_applications.html', {'applications': applications})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Feedback
import json

@login_required  # Ensure only logged-in users can submit feedback
@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')

            # Ensure the message is not empty
            if not message:
                return JsonResponse({"status": "error", "message": "Feedback message cannot be empty."})

            # Create feedback associated with the logged-in user
            feedback = Feedback(user=request.user, message=message)
            feedback.save()
            return JsonResponse({"status": "success", "message": "Feedback submitted successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method."})



#
from django.shortcuts import render, redirect
from .models import Survey, Question, Option

from django.shortcuts import render
from .models import Survey, SurveyResponse

def surveyform(request):
    surveys = Survey.objects.prefetch_related('question_set__option_set').all()
    completed_surveys = SurveyResponse.objects.filter(user=request.user).values_list('survey_id', flat=True)

    # Add a flag for each survey to indicate if the user has already completed it
    for survey in surveys:
        survey.is_completed = survey.id in completed_surveys

    context = {'surveys': surveys}
    return render(request, 'surveyform.html', context)


# views.py

from django.shortcuts import render, redirect

from .models import Survey, Question, Option, SurveyResponse

from django.shortcuts import get_object_or_404

@login_required
def submit_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)  # This will return a 404 if the survey is not found

    if request.method == "POST":
        for question in survey.question_set.all():
            selected_option_id = request.POST.get(f'selected_option_{question.id}')
            if selected_option_id:
                selected_option = get_object_or_404(Option, id=selected_option_id)
                SurveyResponse.objects.create(
                    user=request.user,
                    survey=survey,
                    question=question,
                    selected_option=selected_option
                )

        # Create the notification after survey submission
        Notification.objects.create(
            user=request.user,
            message='You have submitted a new survey: ' + survey.title,
            is_read=False
        )

        return redirect('surveyform')

    return render(request, 'surveyform.html', {'survey': survey})


from django.http import JsonResponse
from django.shortcuts import render
from .models import Notification


from django.shortcuts import render
from .models import Notification

from django.http import JsonResponse

from django.shortcuts import render
from .models import Notification
import pytz

@login_required
def notifications_view(request):
    nepal_tz = pytz.timezone('Asia/Kathmandu')
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
     
     
    for notification in notifications:
        notification.created_at = notification.created_at.astimezone(nepal_tz)
    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Create a list of notification messages and their created_at dates
        notifications_list = [
            {
                'message': notification.message,
                'created_at': notification.created_at.strftime("%d %b %Y %H:%M"),
            }
            for notification in notifications
        ]
        
        # Return JSON response with new count and notifications
        return JsonResponse({
            'new_count': unread_count,
            'notifications': notifications_list,
        })

    # Regular request: render the full notifications page or template
    return render(request, 'newsfeed.html', {'notifications': notifications, 'unread_count': unread_count})




from django.http import JsonResponse


@login_required
def mark_notifications_as_read(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


# janajodapp/context_processors.py
from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('login')