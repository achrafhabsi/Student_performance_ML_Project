from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from .models import Student

def train_knn_model():
    students = Student.objects.all()
    X = []
    y = []
    for student in students:
        X.append([student.age, student.Medu, student.Fedu, student.traveltime, student.studytime,
                  student.failures, student.famrel, student.freetime, student.goout, student.Dalc, student.Walc,
                  student.health, student.absences, student.G1, student.G2])
        y.append(student.G3)
    
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)
    
    return knn
