from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    # path('signup/seller/', InstructorSignUpSerializer.as_view(), name='signup-instructor'),
    # path('signup/buyer/', StudentSignUpSerializer.as_view(), name='signup-student'),
    path('signup/', StudentSignUp.as_view(), name='auth_register'),
    # path('login/', login),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('courses', CourseApiView.as_view(), name='token_refresh'),
    path('course/<int:course_id>', CourseDetailApiView.as_view(), name='token_refresh'),
    path('section/<int:section_id>/<int:student_id>/<str:mac>', sectionDetailApiView.as_view()),
    path('section/enroll/<int:section_id>', EnrolledSectionApiView.as_view()),
    path('codes/', EnrollmentCodeApiView.as_view()),
    path('codes/sold/<int:code_id>', EnrollmentCodeApiView.as_view()),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair')

]