from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('custom-admin/', views.custom_admin_home, name='custom_admin_home'),
      path('add_user/', views.add_user, name='add_user'),
     path('user-list/', views.user_list, name='user_list'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
     path('committee-members/', views.committee_member_list, name='committee_members'),
      path('committee-members/edit/<int:pk>/', views.edit_committee_member, name='edit_committee_member'),
    path('committee-members/delete/<int:pk>/', views.delete_committee_member, name='delete_committee_member'),
    path('admin-complain/', views.admin_complain, name='admin_complain'), 
    path('add-complaint/', views.add_complaint, name='add_complaint'),
     path('complaints/show/<int:complaint_id>/', views.show_complaint, name='show_complaint'),
     path('complaints/edit/<int:complaint_id>/', views.edit_complaint, name='edit_complaint'),
    path('complaints/delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    # path('adminevent/', views.adminevent, name='adminevent'),
    path('adminevents/', views.admin_events, name='admin_events'),
    path('adminevents/add/', views.add_event, name='add_event'),
    path('adminevents/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('adminevents/approve/<int:event_id>/', views.approve_event, name='approve_event'),
    path('adminevents/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('userreqevent/', views.userreqevent_list, name='userreqevent_list'),
    path('userreqevent/add/', views.userreqevent_add, name='userreqevent_add'),
    path('userreqevent/edit/<int:pk>/', views.userreqevent_edit, name='userreqevent_edit'),
    path('userreqevent/delete/<int:pk>/', views.userreqevent_delete, name='userreqevent_delete'),
     path('profilemanage/', views.profilemanage, name='profilemanage'),
    path('profilemanage/edit/<int:pk>/', views.edit_profile, name='edit_profile'),
    path('profilemanage/confirm-delete/<int:pk>/', views.confirm_delete_profile, name='confirm_delete_profile'),
    path('profilemanage/delete/<int:pk>/', views.delete_profile, name='delete_profile'),
     
     path('viewservicerequests/', views.view_service_requests, name='view_service_requests'),
   
    # path('viewservicerequest/add/', views.add_service_request, name='add_service_request'),
    path('viewservicerequest/<int:id>/', views.view_service_request_detail, name='service_request_detail'),
     path('viewservicerequests/add/', views.add_service_request, name='add_service_request'),
   path('viewservicerequest/delete/<int:pk>/', views.delete_service_request, name='delete_service_request'),
    path('viewservicerequest/confirm-delete/<int:pk>/', views.confirm_delete_service_request, name='confirm_delete_service_request'),

    path('viewpostadmin/', views.viewpostadmin, name='viewpostadmin'),
    path('adminedit_post/<int:post_id>/', views.adminedit_post, name='adminedit_post'),
    path('admindelete_post/<int:post_id>/', views.admin_delete_post, name='admindelete_post'),

    path('adminadd-post/', views.admin_add_post, name='admin_add_post'),
    
     path('feedback/', views.show_feedback, name='showfeedback'),
    path('feedback/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
     path('adminjob-applications/', views.admin_job_applications, name='admin_job_applications'),
    path('adminjob-applications/add/', views.add_job_application, name='add_job_application'),
    
    path('adminjob-applications/edit/<int:pk>/', views.edit_job_application, name='edit_job_application'),
   
    path('adminjob-applications/delete/<int:pk>/', views.delete_job_application, name='delete_job_application'),
    path('post_job/', views.admin_post_job, name='admin_post_job'),
    path('adminjobs/', views.admin_job_list, name='admin_job_list'), 
    path('adminjobs/edit/<int:job_id>/', views.admin_edit_job, name='admin_edit_job'),
    path('adminjobs/delete/<int:job_id>/', views.admin_delete_job, name='admin_delete_job'),# Job listing page
     path('userreqjob/', views.UserReqJobListView.as_view(), name='userreqjob_list'),
    path('userreqjob/add/', views.UserReqJobCreateView.as_view(), name='userreqjob_add'),
    path('userreqjob/<int:pk>/change/', views.UserReqJobUpdateView.as_view(), name='userreqjob_change'),
    path('userreqjob/<int:pk>/delete/', views.UserReqJobDeleteView.as_view(), name='userreqjob_delete'),
   
      
    path('login/', auth_views.LoginView.as_view(template_name ='login.html',
                                                redirect_authenticated_user=False), name='login'),
    
    
    path('', views.home, name="home"),
    path('wardpost/', views.wardpost, name="wardpost"),
     path('events/', views.events, name='events'),
    path('announce/', views.job_listings, name="announce"),
    path('create-announcement/', views.create_announcement, name='create_announcement'),
    #  path('jobs/', job_listings, name='job_listings'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('servicerequest/', views.servicerequest, name="servicerequest"),
    path('complain/', views.complain, name="complain"),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('user-job-applications/', views.user_job_applications_view, name='user_job_applications'),
    # path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('submit_event/', views.submit_event, name='submit_event'),
    path('surveyform/', views.surveyform, name='surveyform'),
    path('submit-survey/<int:survey_id>/', views.submit_survey, name='submit_survey'),
     path('notifications/', views.notifications_view, name='notifications'),
    path('mark_notifications_as_read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    #register
    path('register/',views.register,name='register'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'), 
     path('delete-post/<int:id>/', views.delete_post, name='delete_post'),
    # path('profile/',views.profile,name='profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
     path('profile/', views.profile, name='profile'),
    #login view 
     path('logout/', views.logout_view, name='logout'),
    
    #logout
    #  path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    

    #for activate account through mail using link
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),


    #for reset password
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),

    #for password reset done
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),

    #for password reset confirm
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),

    #for password reset complete
    path('password_reset_complete,/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)