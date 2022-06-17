from django.urls import path, include
from .views import LoginView, IndexView, LogoutView, CourseListView, CourseCreateView, LessonCreateView, \
    SectionCreateView, CourseBySectionListView, SectionListView, SectionRetrieveView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', IndexView.as_view(), name="home"),
    path('course/', include([
        path('list/', CourseListView.as_view(), name="course-list"),
        path('create/', CourseCreateView.as_view(), name="course-create"),
        path('<int:course_id>/', CourseBySectionListView.as_view(), name='course-by-section-list'),
    ])),
    path('section/', include([
        path('list/', SectionListView.as_view(), name='section-list'),
        path('<int:pk>/', SectionRetrieveView.as_view(), name='section-detail'),
        path('create/', SectionCreateView.as_view(), name='section-create')
    ])),
    path('lesson/create/', LessonCreateView.as_view(), name='lesson-create')
]
