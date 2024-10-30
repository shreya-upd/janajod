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
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, PostForm
from django.contrib import messages
from .models import Post

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

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Unliking
    else:
        post.likes.add(request.user)  # Liking
    
    # Redirect to the referring page
    return redirect(request.META.get('HTTP_REFERER', 'default_url_if_none'))  # Use a default URL if no referrer is found

from django.shortcuts import get_object_or_404, redirect

def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)  # Remove dislike
    else:
        post.dislikes.add(request.user)  # Add dislike
    
    # Redirect to the referring page or a specific URL
    return redirect(request.META.get('HTTP_REFERER', 'default_url_if_none'))  # Use default if no referrer


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm


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
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Event

from django.shortcuts import render
from .models import UserEventRequest

from django.shortcuts import render
from .models import UserEventRequest, Event
from django.db.models import Q

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
from django.contrib.auth.decorators import login_required
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
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Job, UserReqJob

@login_required
def job_listings(request):
    jobs = Job.objects.all().order_by('-posted_on')
    applied_jobs = JobApplication.objects.filter(user=request.user).values_list('job_id', flat=True)
    
    # Fetch approved UserReqJob entries
    approved_user_req_jobs = UserReqJob.objects.filter(is_approved=True).order_by('-posted_on')
    admin_posted_jobs = Job.objects.all().order_by('-posted_on') 
    
    return render(request, 'announce.html', {
        'jobs': jobs,
        'applied_jobs': applied_jobs,
        'admin_posted_jobs': admin_posted_jobs,
        'approved_user_req_jobs': approved_user_req_jobs
    })



@login_required
def apply_for_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        applicant_name = request.POST['fullname']
        contact_number = request.POST['contactNumber']
        address = request.POST['address']
        email = request.POST['email']
        why_this_job = request.POST['whyThisJob']

        # Create a new job application
        JobApplication.objects.create(
            job=job,
            applicant_name=applicant_name,
            contact_number=contact_number,
            address=address,
            email=email,
            why_this_job=why_this_job,
            user=request.user  # Associate the application with the current user
        )
        
        # Redirect or render a success message
        return redirect('announce')

    return render(request, 'announce', {'job': job})

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



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
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
from django.contrib.auth.decorators import login_required
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


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .models import Notification

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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
from django.contrib.auth.decorators import login_required

@login_required
def mark_notifications_as_read(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
