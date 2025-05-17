from django import forms
from .models import Student, Teacher, Admin, User, Class

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'user_type']
        widgets = {
            'password': forms.PasswordInput(),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'familyname', 'phone', 'address', 'hiredate', 'subject', 'classes']
        widgets = {
            'hiredate': forms.DateInput(attrs={'type': 'date'}),
        }


from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'familyname', 'teacher', 'class_name', 'age', 'sex', 'famsize', 'Pstatus', 
                  'Medu', 'Fedu', 'Mjob', 'Fjob', 'reason', 'guardian', 'schoolsup', 'famsup', 
                  'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic', 'traveltime', 
                  'studytime', 'failures', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 
                  'absences']

    # Use the choices defined in the model directly
    sex = forms.ChoiceField(choices=[(1, 'Male'), (2, 'Female')])
    famsize = forms.ChoiceField(choices=[(1, 'LE3'), (2, 'GT3')])
    Pstatus = forms.ChoiceField(choices=[(1, 'Living Together'), (2, 'Apart')])
    Medu = forms.ChoiceField(choices=[(0, 'None'), (1, 'Primary'), (2, '5th to 9th'), (3, 'Secondary'), (4, 'Higher')])
    Fedu = forms.ChoiceField(choices=[(0, 'None'), (1, 'Primary'), (2, '5th to 9th'), (3, 'Secondary'), (4, 'Higher')])
    Mjob = forms.ChoiceField(choices=[(1, 'Teacher'), (2, 'Health Care'), (3, 'Civil Services'), (4, 'At Home'), (5, 'Other')])
    Fjob = forms.ChoiceField(choices=[(1, 'Teacher'), (2, 'Health Care'), (3, 'Civil Services'), (4, 'At Home'), (5, 'Other')])
    reason = forms.ChoiceField(choices=[(1, 'Close to Home'), (2, 'Reputation'), (3, 'Course Preference'), (4, 'Other')])
    guardian = forms.ChoiceField(choices=[(1, 'Mother'), (2, 'Father'), (3, 'Other')])
    schoolsup = forms.ChoiceField(choices=[(1, 'Yes'), (2, 'No')])
    famsup = forms.ChoiceField(choices=[(1, 'Yes'), (2, 'No')])
    paid = forms.ChoiceField(choices=[(1, 'Yes'), (2, 'No')])
    activities = forms.ChoiceField(choices=[(1, 'Yes'), (2, 'No')])
    nursery = forms.ChoiceField(choices=[(1, 'Yes'), (2, 'No')])
    higher = forms.ChoiceField(choices=[(1, 'Yes'), (2, 'No')])
    internet = forms.ChoiceField(choices=[(1, 'Yes'), (2, 'No')])
    romantic = forms.ChoiceField(choices=[(1, 'Yes'), (2, 'No')])
    traveltime = forms.ChoiceField(choices=[(1, '<15 min'), (2, '15-30 min'), (3, '30 min-1 hour'), (4, '>1 hour')])
    studytime = forms.ChoiceField(choices=[(1, '<2 hours'), (2, '2-5 hours'), (3, '5-10 hours'), (4, '>10 hours')])
    failures = forms.ChoiceField(choices=[(1, '1 failure'), (2, '2 failures'), (3, '3 failures'), (4, '4 or more failures')])
    famrel = forms.ChoiceField(choices=[(1, 'Very bad'), (2, 'Bad'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')])
    freetime = forms.ChoiceField(choices=[(1, 'Very low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Very high')])
    goout = forms.ChoiceField(choices=[(1, 'Very low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Very high')])
    Dalc = forms.ChoiceField(choices=[(1, 'Very low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Very high')])
    Walc = forms.ChoiceField(choices=[(1, 'Very low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Very high')])
    health = forms.ChoiceField(choices=[(1, 'Very bad'), (2, 'Bad'), (3, 'Average'), (4, 'Good'), (5, 'Very good')])


# Form for Login
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())



# Form for updating student data
class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'familyname', 'class_name', 'age', 'Medu', 'Fedu', 'traveltime', 'studytime',
                  'failures', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G3']

# Form for updating teacher data
class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name','classes','familyname','phone','address','hiredate','subject']

# Form for updating user data (email, password, etc.)
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
# Form for updating teacher data

class ClassUpdateForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name']