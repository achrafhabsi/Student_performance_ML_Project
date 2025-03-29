from django.shortcuts import render, redirect
from .models import User, Student, Teacher, Admin
from .forms import LoginForm, StudentForm, TeacherForm
import numpy as np
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .utils import train_knn_model
from django.shortcuts import render, redirect
from .models import User, Student, Teacher, Admin, Message
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Login view
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email, password=password)
                if user.user_type == 'student':
                    return redirect(f'/student/{user.student.id}/dashboard/')
                elif user.user_type == 'teacher':
                    return redirect(f'/teacher/{user.id}/dashboard/')
                elif user.user_type == 'admin':
                    return redirect(f'/ads/{user.admin.id}/dashboard/')
            except User.DoesNotExist:
                # Handle incorrect login
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


from django.shortcuts import render
from .models import Student
from django.db.models import Avg

def student_dashboard(request, student_id):
    stx = student_id - 2
    student = Student.objects.get(id=stx)

    # Get all students in the same class
    class_students = Student.objects.filter(class_name=student.class_name)

    # Calculate mean values for absences, study time, and G3 score in the same class
    mean_absences = class_students.aggregate(Avg('absences'))['absences__avg']
    mean_studytime = class_students.aggregate(Avg('studytime'))['studytime__avg']
    mean_G3 = class_students.aggregate(Avg('G3'))['G3__avg']

    # Pass student data and calculated mean values to the template
    return render(request, 'student_dashboard.html', {
        'student': student,
        'mean_absences': mean_absences,
        'mean_studytime': mean_studytime,
        'mean_G3': mean_G3,
    })


from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Teacher, Student, Message

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Teacher, Student, Message
from django.db.models import Q

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Count, Q
from .models import Teacher, Student, Message

def teacher_dashboard(request, user_id):
    # Get the teacher based on user_id
    teacher = get_object_or_404(Teacher, user_id=user_id)

    # Fetch all students associated with this teacher
    students = Student.objects.filter(teacher=teacher)

    # Categorize students based on their results
    students_zero = students.filter(result=0).count()  # Students with result 0
    students_one = students.filter(result=1).count()  # Students with result 1
    students_other = students.exclude(result__in=[0, 1]).count()  # Students with other results

    # Fetch all messages related to the teacher
    messages = Message.objects.filter(
        Q(sender__email=request.user.email) | Q(recipient__email=request.user.email)
    )

    # Send the categorized data to the template
    return render(request, 'teacher_dashboard.html', {
        'teacher': teacher,
        'students': students,
        'messages': messages,
        'students_zero': students_zero,
        'students_one': students_one,
        'students_other': students_other,
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Student, Teacher, Admin, Message, Class
from .forms import StudentForm, TeacherForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from django.http import JsonResponse


from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .models import Admin, Student, Teacher, Class, Message

def admin_dashboard(request, user_id):
    admin = get_object_or_404(Admin, user_id=user_id)
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    classes = Class.objects.all()

    # Calculate totals
    total_students = students.count()
    total_teachers = teachers.count()
    total_classes = classes.count()

    # Students at risk (result = 0)
    students_at_risk = students.filter(result=0)
    students_at_risk_count = students_at_risk.count()
    students_not_at_risk_count = total_students - students_at_risk_count

    # Teachers at risk (teaching students with result = 0)
    teachers_at_risk_count = teachers.filter(student__result=0).distinct().count()
    teachers_not_at_risk_count = total_teachers - teachers_at_risk_count

    # Count students with result = 0 per teacher
    teacher_student_counts = [
        {'teacher': teacher, 'zero_count': students_at_risk.filter(teacher=teacher).count()}
        for teacher in teachers
    ]
    teacher_student_counts.sort(key=lambda x: x['zero_count'], reverse=True)

    if request.method == 'POST' and 'send_message_to_teacher' in request.POST:
        teacher_id = request.POST['teacher']
        message_content = request.POST['message']
        teacher = get_object_or_404(Teacher, id=teacher_id)
        Message.objects.create(
            sender=request.user,
            recipient=teacher.user,
            content=message_content,
            message_type='admin_to_teacher'
        )

    return render(request, 'admin_dashboard.html', {
        'admin': admin,
        'students': students,
        'teachers': teachers,
        'classes': classes,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'students_at_risk_count': students_at_risk_count,
        'students_not_at_risk_count': students_not_at_risk_count,
        'teachers_at_risk_count': teachers_at_risk_count,
        'teachers_not_at_risk_count': teachers_not_at_risk_count,
        'teacher_student_counts': teacher_student_counts,
        'students_with_zero_result': students_at_risk,
    })


from django.http import HttpResponse


from .models import Student, Message





from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
import io


def generate_report(request, student_id):
    # Fetch student data
    student = get_object_or_404(Student, id=student_id)

    # Fetch student messages (if any)
    messages = Message.objects.filter(recipient=student.user)
    message_content = "\n".join([f"{msg.sent_at.strftime('%Y-%m-%d')} - {msg.content}\n" for msg in messages]) if messages.exists() else "No recommendations available."

    # Prepare the data dictionary for the HTML template
    form_data = {
        "name": student.name,
        "familyname": student.familyname,
        "teacher": student.teacher.name,
        "class_name": student.class_name.name,
        "age": student.age,
        "sex": student.sex,
        "guardian": student.guardian,
        "address": student.address,
        "famsize": student.famsize,
        "Pstatus": student.Pstatus,
        "Medu": student.Medu,
        "Fedu": student.Fedu,
        "Mjob": student.Mjob,
        "Fjob": student.Fjob,
        "reason": student.reason,
        "traveltime": student.traveltime,
        "studytime": student.studytime,
        "failures": student.failures,
        "famrel": student.famrel,
        "freetime": student.freetime,
        "goout": student.goout,
        "Dalc": student.Dalc,
        "Walc": student.Walc,
        "health": student.health,
        "absences": student.absences,
        "schoolsup": student.schoolsup,
        "famsup": student.famsup,
        "paid": student.paid,
        "activities": student.activities,
        "nursery": student.nursery,
        "higher": student.higher,
        "internet": student.internet,
        "romantic": student.romantic,
        "G1": student.G1,
        "G2": student.G2,
        "messages": message_content,
    }

    # Render the HTML template with the data
    html_string = render_to_string('student_report_template.html', form_data)

    # Convert the HTML to PDF
    pdf_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html_string), dest=pdf_file)
    
    if pisa_status.err:
        return HttpResponse("Error generating PDF", content_type="text/plain")

    # Return the PDF as a response
    pdf_file.seek(0)
    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="student_report_{student_id}.pdf"'
    
    return response



# Generate Report for Teacher's Class (Teacher)
def generate_teacher_report(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    students = Student.objects.filter(teacher=teacher)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{teacher.name}_report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Teacher Report: {teacher.name}")
    p.drawString(100, 730, f"Subject: {teacher.subject}")
    p.drawString(100, 710, f"Number of Students: {students.count()}")
    p.showPage()
    p.save()
    return response

# Student Views



from django.shortcuts import render, redirect
from .models import Message, Teacher
from django.contrib.auth import get_user_model

User = get_user_model()

def send_message_to_teacher(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        message_content = request.POST.get('message')

        # Check if teacher_id and message_content are provided
        if teacher_id and message_content:
            try:
                # Fetch the teacher instance using the provided teacher_id
                teacher = Teacher.objects.get(id=teacher_id)

                # Explicitly resolve the user instance from request.user
                sender = User.objects.get(id=request.user.id)  # Ensure it's a User instance

                # Create the message and assign sender and recipient
                message = Message(
                    sender=sender,  # sender is now a proper User instance
                    recipient=teacher.user,  # recipient is the associated User instance of the teacher
                    content=message_content,  # content is the message passed in the form
                    message_type='admin_to_teacher'  # Specify the type of message
                )
                message.save()  # Save the message to the database

                # Redirect to the admin dashboard page with the user_id of the logged-in user
                return redirect('admin_dashboard', user_id=request.user.id)

            except Teacher.DoesNotExist:
                # If the teacher does not exist, render an error page with the appropriate message
                return render(request, "error.html", {"error": "Teacher not found"})

    # If the request method isn't POST, or if the message sending failed, redirect to the admin dashboard
    return redirect('admin_dashboard', user_id=request.user.id)

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .models import Message, Student

User = get_user_model()

def send_message_to_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        
        message_content = request.POST.get('message')

        if not student_id or not message_content:
            return render(request, "error.html", {"error": "Student or message content missing"})

        try:
            student = Student.objects.get(id=student_id)
            teacher= Teacher.objects.get(id=request.user.id)
            

            Message.objects.create(
                sender=teacher.user,
                recipient=student.user,
                content=message_content,
                message_type='teacher_to_student'
            )

            return redirect('teacher_dashboard', user_id=request.user.id + 1)

        except Student.DoesNotExist:
            return render(request, "error.html", {"error": "Student not found"})

    return redirect('teacher_dashboard', user_id=request.user.id + 1)

# Helper to get all messages for a user
def get_received_messages(user):
    return Message.objects.filter(recipient=user).order_by('-sent_at')

from django.shortcuts import render, get_object_or_404
from .models import Message, Admin

from django.shortcuts import render, get_object_or_404
from .models import Message, Admin
from django.contrib.auth.models import User

def get_sended_messages(request, admin_id):
    admin = Admin.objects.get(user_id=admin_id)
    teachers = Teacher.objects.all()

    # Ensure request.user is a User instance
    if not isinstance(request.user, User):
        return render(request, 'ads_messages.html', {'error': 'Invalid user session'})

    # Fetch messages sent by the logged-in user
    sent_messages = Message.objects.filter(sender=request.user).order_by('-sent_at')
    
    if request.method == 'POST':
        # Sending message to teacher
        if 'send_message_to_teacher' in request.POST:
            teacher_id = request.POST['teacher']
            message_content = request.POST['message']
            teacher = Teacher.objects.get(id=teacher_id)
            message = Message(sender=request.user, recipient=teacher.user, content=message_content, message_type='admin_to_teacher')
            message.save()

    return render(request, 'ads_messages.html', {'admin': admin, 'teachers': teachers, 'sent_messages': sent_messages,})



from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Student, Teacher, Admin, Message
from .forms import LoginForm, StudentForm, TeacherForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Login view

# Admin Dashboard View

from django.shortcuts import render, redirect
from .forms import TeacherForm, StudentForm, UserForm
from .models import User

def create_teacher(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'teacher'  # Assign user type
            user.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            teacher_form.save_m2m()  # Save many-to-many classes
            return redirect('teacher_list')  # Redirect after successful creation
    else:
        user_form = UserForm()
        teacher_form = TeacherForm()

    return render(request, 'create_teacher.html', {'user_form': user_form, 'teacher_form': teacher_form})

def create_student(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'student'  # Assign user type
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            return redirect('student_list')  # Redirect after successful creation
    else:
        user_form = UserForm()
        student_form = StudentForm()

    return render(request, 'create_student.html', {'user_form': user_form, 'student_form': student_form})


def create_class(request):
    """Render the create class form and handle submissions."""
    if request.method == "POST":
        class_name = request.POST.get("name")
        if class_name:
            new_class, created = Class.objects.get_or_create(name=class_name)
            if created:
                return redirect('create_class')  # Redirect after successful creation
            else:
                return JsonResponse({"error": "Class already exists."}, status=400)
    return render(request, 'create_class.html')

    

from django.shortcuts import render
from .models import Student  # Import your Student model

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students_list.html', {'students': students})


from django.shortcuts import render
from .models import Teacher  # Import your Student model

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers_list.html', {'teachers': teachers})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Teacher, User
from .forms import StudentUpdateForm, TeacherUpdateForm, UserUpdateForm

def student_update(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_update', student_id=student.id)  # Redirect to the student's profile or dashboard
    else:
        form = StudentUpdateForm(instance=student)
    return render(request, 'student_update.html', {'form': form})

def teacher_update(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = TeacherUpdateForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_update', teacher_id=teacher.id)  # Redirect to the teacher's dashboard
    else:
        form = TeacherUpdateForm(instance=teacher)
    return render(request, 'teacher_update.html', {'form': form})

def admin_update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('ads_student_update', student_id=student.id)  # Redirect to the student's profile or dashboard
    else:
        form = StudentUpdateForm(instance=student)
    return render(request, 'ads_student_update.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher
from .forms import TeacherUpdateForm

def admin_update_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = TeacherUpdateForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('ads_teacher_update', teacher_id=teacher.id)  # Redirect to the teacher's dashboard
    else:
        form = TeacherUpdateForm(instance=teacher)
    return render(request, 'ads_teacher_update.html', {'form': form})

from django.shortcuts import render
import pickle



import pickle
import numpy as np
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Student

# Helper function to load the model
def load_model():
    with open('random_forest_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

def predict_student_result(request, student_id):
    # Load the model
    model = load_model()

    # Retrieve student data
    student = get_object_or_404(Student, id=student_id)

    # Prepare the data for prediction
    features = [
        student.age,
        student.Medu,
        student.Fedu,
        student.traveltime,
        student.studytime,
        student.failures,
        student.famrel,
        student.freetime,
        student.goout,
        student.Dalc,
        student.Walc,
        student.health,
        student.absences,
        student.G1,  # Grade 3 (target variable)
        
        # Raw categorical variables (no encoding needed)
        student.sex,  # Assuming 'sex' is a numeric or categorical field already in the correct format
        student.famsize,  # Assuming 'famsize' is in a valid format (e.g., 'LE3', 'GT3')
        student.Pstatus,  # Assuming 'Pstatus' is in a valid format (e.g., 'T', 'A')
        student.Mjob,  # Assuming 'Mjob' is a valid field (e.g., 'teacher', 'health', etc.)
        student.Fjob,  # Assuming 'Fjob' is a valid field (e.g., 'teacher', 'health', etc.)
        student.reason,  # Assuming 'reason' is a valid field (e.g., 'course', 'home', etc.)
        student.guardian,  # Assuming 'guardian' is a valid field (e.g., 'mother', 'father', etc.)
        student.schoolsup,  # Assuming 'schoolsup' is a valid field (e.g., 'yes', 'no')
        student.famsup,  # Assuming 'famsup' is a valid field (e.g., 'yes', 'no')
        student.paid,  # Assuming 'paid' is a valid field (e.g., 'yes', 'no')
        student.activities,  # Assuming 'activities' is a valid field (e.g., 'yes', 'no')
        student.nursery,  # Assuming 'nursery' is a valid field (e.g., 'yes', 'no')
        student.higher,  # Assuming 'higher' is a valid field (e.g., 'yes', 'no')
        student.internet,  # Assuming 'internet' is a valid field (e.g., 'yes', 'no')
        student.romantic  # Assuming 'romantic' is a valid field (e.g., 'yes', 'no')
    ]

    # Make the prediction using the model
    prediction = model.predict([features])

    # Convert the prediction (which may be int64) to native int type
    prediction_value = int(prediction[0])

    # Save the result to the student's result field
    student.result = prediction_value
    student.save()

    # Return a response (you can customize this as needed)
    return JsonResponse({'student_id': student_id, 'prediction': prediction_value})






from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Class
from .forms import ClassUpdateForm

def admin_update_class(request, class_name):
    class_instance = get_object_or_404(Class, name=class_name)

    if request.method == 'POST':
        form = ClassUpdateForm(request.POST, instance=class_instance)
        if form.is_valid():
            form.save()

            # Handle AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Class updated successfully', 'status': 'success'})

            return redirect('ads_class_update', class_name=class_instance.name)  # Ensure this URL name exists
    else:
        form = ClassUpdateForm(instance=class_instance)

    return render(request, 'ads_class_update.html', {'form': form, 'class_instance': class_instance})

   

def delete_student(request, student_id):
    """Delete a student by ID."""
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return JsonResponse({"message": "Student deleted successfully."})

def delete_teacher(request, teacher_id):
    """Delete a teacher by ID."""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.delete()
    return JsonResponse({"message": "Teacher deleted successfully."})

def delete_class(request, class_name):
    """Delete a class by name."""
    class_instance = get_object_or_404(Class, name=class_name)
    class_instance.delete()
    return JsonResponse({"message": "Class deleted successfully."})

