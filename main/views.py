import time

from django.contrib import messages
from django.db import transaction
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView

from config.decorators import unauthenticated_user, authenticated_user
from config.mixins import LoginRequired

from main.forms import LoginForm, CourseForm, LessonForm, SectionForm, LessonCreateForm
from main.models import Course, Section, Lesson
from main.tasks import lesson_save


class LoginView(generic.TemplateView):

    @method_decorator(unauthenticated_user)
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', context={'form': form})

    @method_decorator(unauthenticated_user)
    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "username and/or password incorrect")
        return render(request, 'login.html', context={'form': form})


class LogoutView(LoginRequired, generic.TemplateView):
    @method_decorator(authenticated_user)
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class IndexView(LoginRequired, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class CourseListView(LoginRequired, generic.ListView):
    template_name = 'course/list.html'
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)


class CourseBySectionListView(LoginRequired, generic.ListView):
    template_name = 'section/course-by-list.html'
    context_object_name = 'sections'

    def get_queryset(self):
        return Section.objects.filter(course_id=self.kwargs.get('course_id'))


class SectionListView(LoginRequired, generic.ListView):
    template_name = 'section/list.html'
    context_object_name = 'sections'

    def get_queryset(self):
        return Section.objects.filter(course__teacher=self.request.user)


class SectionRetrieveView(LoginRequired, generic.DetailView):
    template_name = 'section/retrieve.html'
    context_object_name = 'section'

    def get_object(self, queryset=None):
        return get_object_or_404(Section, id=self.kwargs.get('pk'))


class CourseCreateView(LoginRequired, generic.CreateView):
    form_class = CourseForm
    template_name = 'course/create.html'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.teacher = self.request.user
        form.save()
        return redirect('course-list')


class SectionCreateView(LoginRequired, generic.CreateView):
    form_class = SectionForm
    template_name = 'section/create.html'
    success_url = '/section/create/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class LessonCreateView(LoginRequired, TemplateView):
    def get(self, request, *args, **kwargs):
        form = LessonForm(user=request.user)
        return render(request, 'lesson/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        start1 = time.time()
        file = request.FILES.get('file')
        # print(time.time() - start1)
        form = LessonCreateForm(data=request.POST, user=self.request.user)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            section_id = form.cleaned_data.get('section').id
            # with transaction.atomic():
            #     file_path = "media/" + file.name
            #     lesson = Lesson.objects.create(
            #         name=form.cleaned_data.get('name'),
            #         section=form.cleaned_data.get('section'),
            #     )
            #     with open(file_path, 'wb+') as f:
            #         for chunk in file.chunks():
            #             f.write(chunk)
            #         f.close()
            #     lesson.file = file.name
            #     lesson.save()
            return redirect('lesson-create')
        return render(request, 'lesson/create.html', {'form': form})
