from django.urls import path, re_path, include
from django.conf import settings

from rest_framework.authtoken import views as rf_auth_views
from rest_framework.documentation import include_docs_urls

from rest_framework import routers
import coreapi
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'trainees', views.TraineeViewSet)
router.register(r'mentors', views.MentorViewSet)
router.register(r'submentors', views.SubMentorViewSet)
router.register(r'queries', views.QueryViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'modules', views.ModuleViewSet)
router.register(r'lessons', views.LessonViewSet)
# router.register(r'exams', views.ExamViewSet)
router.register(r'examsubmissions', views.ExamSubmissionViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'projectsubmissions', views.ProjectSubmissionViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'answerchoices', views.AnswerChoiceViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'tests', views.TestViewSet)


urlpatterns = [
    path('user/<username>', views.user_detail, name='user_detail'),
    path('signup', views.signup, name='signup'),
    path('signup/trainee', views.signup_trn, name='signup_trn'),
    path('signup/trainee/user', views.signup_trn_user, name='signup_trn_user'),
    path('signup/trainee/profile', views.signup_trn_profile, name='signup_trn_profile'),
    path('signup/trainee/personality', views.signup_trn_personality, name='signup_trn_personality'),
    path('signup/trainee/personality/test', views.signup_trn_personality_test, name='signup_trn_personality_test'),
    path('signup/trainee/iq', views.signup_trn_iq, name='signup_trn_iq'),
    path('signup/trainee/iq/test/<int:test_pk>', views.signup_trn_iq_test, name='signup_trn_iq_test'),
    path('signup/trainee/verbal-ability', views.signup_trn_vat, name='signup_trn_vat'),
    path('signup/trainee/verbal-ability/test/<int:test_pk>', views.signup_trn_vat_test, name='signup_trn_vat_test'),
    path('signup/trainee/social', views.signup_trn_social, name='signup_trn_social'),
    path('signup/trainee/complete', views.signup_trn_complete, name='signup_trn_complete'),
    path('signup/mentor', views.signup_men, name='signup_men'),
    path('signup/mentor/user', views.signup_men_user, name='signup_men_user'),
    path('signup/mentor/profile', views.signup_men_profile, name='signup_men_profile'),
    path('signup/mentor/skills', views.signup_men_skills, name='signup_men_skills'),
    path('signup/mentor/account', views.signup_men_account, name='signup_men_account'),
    path('signup/mentor/social', views.signup_men_social, name='signup_men_social'),
    path('signup/mentor/complete', views.signup_men_complete, name='signup_men_complete'),

    path('signup/SubMentor', views.signup_submen, name='signup_submen'),
    path('signup/SubMentor/user', views.signup_submen_user, name='signup_submen_user'),
    path('signup/SubMentor/profile', views.signup_submen_profile, name='signup_submen_profile'),
    path('signup/SubMentor/skills', views.signup_submen_skills, name='signup_submen_skills'),
    path('signup/SubMentor/account', views.signup_submen_account, name='signup_submen_account'),
    path('signup/SubMentor/social', views.signup_submen_social, name='signup_submen_social'),
    path('signup/SubMentor/complete', views.signup_submen_complete, name='signup_submen_complete'),

    path('password_reset_form', views.password_reset_form, name='password_reset_form'),
    path('password_reset_done', views.password_reset_done, name='password_reset_done'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/submentor/requests/', views.request_page,name='request_page'),
    path('dashboard/submentor/requests/accept/<nameofacceptedguy>', views.accept_page,name='accept_page'),
    
    path('profile/', views.profile, name='profile'),
    path('settings/profile', views.profile_settings, name='profile_settings'),
    path('settings/account', views.account_settings, name='account_settings'),
    path('settings/email', views.email_settings, name='email_settings'),
    path('settings/notification ', views.notification_settings, name='notification_settings'),
    path('forum/', views.forum, name='forum'),
    path('forum/query/<int:query_pk>', views.query_detail, name='query_detail'),
    path('forum/query/new', views.query_new, name='query_new'),
    path('courses/list', views.course_list, name='course_list'),
    path('courses/<int:course_pk>/about', views.course_about, name='course_about'),
    path('courses/<int:course_pk>/start', views.course_start, name='course_start'),
    path('courses/<int:course_pk>/modules/<int:module_id>', views.module_about, name='module_about'),
    path('courses/<int:course_pk>/modules/<int:module_id>/lessons/<int:lesson_id>', views.lesson_detail,
         name='lesson_detail'),
    path('projects/list', views.project_list, name='project_list'),
    path('projects/<int:project_pk>', views.project_about, name='project_about'),
    path('projects/<int:project_pk>/dashboard', views.project_detail, name='project_detail'),
    path('mod/settings/', views.mod_settings, name='mod_settings'),
    path('mod/settings/tags', views.mod_settings_tags, name='mod_settings_tags'),
    path('api/'+str(settings.API_URL), include(router.urls)),
    path('api-auth/'+str(settings.API_URL), include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/'+str(settings.API_URL), rf_auth_views.obtain_auth_token),

    path('api/docs/'+str(settings.API_URL), include_docs_urls(title='LMS API', public=False)),

    path('api/login/'+str(settings.API_URL), views.api_login, name='api_login'),
    path('api/logout/'+str(settings.API_URL), views.api_logout, name='api_logout'),
    path('api/auth-token/'+str(settings.API_URL), views.api_get_auth_token, name='api_auth_token'),
    path('api/hexaco/'+str(settings.API_URL), views.api_hexaco_evaluate, name='api_hexaco_evaluate'),
]
