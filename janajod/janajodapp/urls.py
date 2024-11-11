from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
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
    
    
    #logout
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
    

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