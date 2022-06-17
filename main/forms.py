from django import forms

from main.models import Course, Section, Lesson


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput())


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']


class SectionForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Section
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(teacher=self.user)


class LessonForm(forms.ModelForm):
    section = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['section'].queryset = Section.objects.filter(course__teacher=self.user)

    class Meta:
        model = Lesson
        fields = "__all__"


class LessonCreateForm(forms.ModelForm):
    section = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['section'].queryset = Section.objects.filter(course__teacher=self.user)

    class Meta:
        model = Lesson
        fields = ['name']
