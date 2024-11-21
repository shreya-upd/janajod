

# Register your models here.


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile,Notification

admin.site.unregister(User)  
admin.site.register(User, UserAdmin)  
admin.site.register(Profile)



# janajodapp/admin.py

from django.contrib import admin
from .models import Profile, Post


admin.site.register(Post)



from django.contrib import admin
from .models import Event

admin.site.register(Event)

from django.contrib import admin
from .models import UserEventRequest

@admin.register(UserEventRequest)
class UserEventRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('title', 'description', 'user__username')

# admin.py
from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'location', 'created_at', 'user')
    search_fields = ('fullname', 'location')


from django.contrib import admin
from .models import ServiceRequest

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'location', 'service_type', 'created_at', 'user')  # Customize columns shown in the list view
    search_fields = ('fullname', 'location', 'service_type')  # Add search functionality for specific fields



from django.contrib import admin
from .models import Job, JobApplication

admin.site.register(Job)
admin.site.register(JobApplication)

from django.contrib import admin
from .models import UserReqJob

@admin.register(UserReqJob)
class UserReqJobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'organization', 'posted_on', 'is_approved')  # Update here
    search_fields = ('job_title', 'organization')

from django.contrib import admin
from .models import Feedback

admin.site.register(Feedback)


from django.contrib import admin

from .models import Survey, Question, Option,SurveyResponse

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Option)
# admin.site.register(SurveyResponse)

from django.contrib import admin
from .models import Survey, Question, Option, SurveyResponse
from django.utils.html import format_html

class SurveyResponseAdmin(admin.ModelAdmin):
    # List display for SurveyResponse
    list_display = ('user', 'survey', 'question', 'selected_option', 'submitted_on', 'response_details')
    
    # Adding search functionality to search by user or survey title
    search_fields = ('user__username', 'survey__title', 'question__text', 'selected_option__text')
    
    # Adding filters to make it easier to filter responses based on user or survey
    list_filter = ('survey', 'user', 'question')

    # Create custom function to show response details
    def response_details(self, obj):
        return format_html('<a href="{}">View Details</a>', obj.pk)  # link to the change page for response details

    # Making the 'response_details' a clickable link in the list display
    response_details.short_description = 'Details'

# Register the SurveyResponse model with the custom admin class
admin.site.register(SurveyResponse, SurveyResponseAdmin)


    # other configurations like list_display, list_filter etc. remain as is



from django.contrib import admin
from .models import CommitteeMember

admin.site.register(CommitteeMember)






from django.contrib import admin
from django.contrib.auth.models import User  # Default User model

# Customizing the UserAdmin class for better display
class UserAdmin(admin.ModelAdmin):
    # Define which fields to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login')
    
    # Add search functionality on the user list page
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Add filters on the right-hand side of the user list
    list_filter = ('is_staff', 'is_active')
    
    # Custom actions to activate or deactivate users
    actions = ['activate_users', 'deactivate_users']
    
    # Action to activate selected users
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} user(s) activated.")
    
    # Action to deactivate selected users
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} user(s) deactivated.")
    
    # Short descriptions for custom actions
    activate_users.short_description = "Activate selected users"
    deactivate_users.short_description = "Deactivate selected users"

# Register the User model with the customized UserAdmin class
admin.site.unregister(User)  # Unregister the default User model
admin.site.register(User, UserAdmin)  # Register the User model with the customized admin
