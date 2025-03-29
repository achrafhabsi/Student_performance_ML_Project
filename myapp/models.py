from django.db import models

# User model for common login info
class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    USER_TYPES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin')
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.email


# Class model to associate with students and teachers
class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Teacher model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    classes = models.ManyToManyField(Class, related_name='teachers')
    familyname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    hiredate = models.DateField()
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Admin model (admin can manage both students and teachers)
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    familyname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    hiredate = models.DateField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    familyname = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)

    # Student data (features for prediction)
    age = models.IntegerField(null=True)
    
    # Dropdown Fields (Choices)
    sex = models.IntegerField(choices=[(1, 'Male'), (2, 'Female')], null=True)
    famsize = models.IntegerField(choices=[(1, 'LE3'), (2, 'GT3')], null=True)
    Pstatus = models.IntegerField(choices=[(1, 'Living Together'), (2, 'Apart')], null=True)
    
    # Education levels
    Medu = models.IntegerField(choices=[(0, 'None'), (1, 'Primary'), (2, '5th to 9th'), (3, 'Secondary'), (4, 'Higher')], null=True)
    Fedu = models.IntegerField(choices=[(0, 'None'), (1, 'Primary'), (2, '5th to 9th'), (3, 'Secondary'), (4, 'Higher')], null=True)
    
    # Jobs for parents
    Mjob = models.IntegerField(choices=[(1, 'Teacher'), (2, 'Health Care'), (3, 'Civil Services'), (4, 'At Home'), (5, 'Other')], null=True)
    Fjob = models.IntegerField(choices=[(1, 'Teacher'), (2, 'Health Care'), (3, 'Civil Services'), (4, 'At Home'), (5, 'Other')], null=True)
    
    # Reason for choosing school
    reason = models.IntegerField(choices=[(1, 'Close to Home'), (2, 'Reputation'), (3, 'Course Preference'), (4, 'Other')], null=True)
    
    # Guardian
    guardian = models.IntegerField(choices=[(1, 'Mother'), (2, 'Father'), (3, 'Other')], null=True)
    
    # Support fields (Yes/No choices)
    schoolsup = models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], null=True)
    famsup = models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], null=True)
    paid = models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], null=True)
    activities = models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], null=True)
    nursery = models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], null=True)
    higher = models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], null=True)
    internet = models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], null=True)
    romantic = models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], null=True)
    
    # Time-related fields
    traveltime = models.IntegerField(choices=[(1, '<15 min'), (2, '15-30 min'), (3, '30 min-1 hour'), (4, '>1 hour')], null=True)
    studytime = models.IntegerField(choices=[(1, '<2 hours'), (2, '2-5 hours'), (3, '5-10 hours'), (4, '>10 hours')], null=True)
    
    # Failures
    failures = models.IntegerField(choices=[(1, '1-2 failures'), (4, '3 or more failures')], null=True)
    
    # Relationship and social fields
    famrel = models.IntegerField(choices=[(1, 'Very bad'), (2, 'Bad'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], null=True)
    freetime = models.IntegerField(choices=[(1, 'Very low'), (5, 'Very high')], null=True)
    goout = models.IntegerField(choices=[(1, 'Very low'), (5, 'Very high')], null=True)
    
    # Health-related fields
    Dalc = models.IntegerField(choices=[(1, 'Very low'), (5, 'Very high')], null=True)
    Walc = models.IntegerField(choices=[(1, 'Very low'), (5, 'Very high')], null=True)
    health = models.IntegerField(choices=[(1, 'Very bad'), (5, 'Very good')], null=True)
    
    # Other fields
    absences = models.IntegerField(null=True)
    G3 = models.IntegerField(null=True, default=2)



    # Fields that may be causing the error
    address = models.CharField(max_length=255, null=True, blank=True)
    G2 = models.IntegerField(null=True, blank=True)
    G1 = models.IntegerField(null=True, blank=True)

    result = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.name} {self.familyname}"

# Message model to send messages from Admin to Teacher, and Teacher to Student
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # To track whether the message is read
    MESSAGE_TYPES = (
        ('admin_to_teacher', 'Admin to Teacher'),
        ('teacher_to_student', 'Teacher to Student'),
    )
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)

    def __str__(self):
        return f"Message from {self.sender.email} to {self.recipient.email} on {self.sent_at}"

    class Meta:
        ordering = ['-sent_at']  # Order messages by the most recent first
