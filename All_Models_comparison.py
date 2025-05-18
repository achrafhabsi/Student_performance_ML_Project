import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, roc_curve
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
# Load dataset
df = pd.read_csv("MY_DATA.csv")  # Replace with actual file

# Features and target
X = df.drop(columns=["result"])
X = X.drop(columns=["G3"])
df.replace('U', np.nan, inplace=True)  # Remplace 'U' par NaN
df = df.apply(pd.to_numeric, errors='coerce')  # Convertit tout en numérique
y = df["result"]  # Target variable

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Function to print metrics
def print_metrics(y_test, y_pred, model_name):
    print(f"{model_name} Accuracy:", accuracy_score(y_test, y_pred))
    print(f"{model_name} Precision:", precision_score(y_test, y_pred, average='weighted'))
    print(f"{model_name} Recall:", recall_score(y_test, y_pred, average='weighted'))
    print(f"{model_name} F1-score:", f1_score(y_test, y_pred, average='weighted'))
    print(f"{model_name} Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    
    if len(np.unique(y_test)) == 2:
        roc_auc = roc_auc_score(y_test, y_pred)
        print(f"{model_name} ROC AUC Score:", roc_auc)
        fpr, tpr, _ = roc_curve(y_test, y_pred)
        plt.plot(fpr, tpr, label=f'{model_name} (AUC = {roc_auc:.2f}')

# ---------------------- KNN MODEL ----------------------
knn = KNeighborsClassifier()
param_grid = {"n_neighbors": [3, 5, 7, 9,40,50,60,70,80,90,100,110,120,140,160,180,200,500,1000,2000,3000,4000,5000]}
grid_knn = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')
grid_knn.fit(X_train_scaled, y_train)
y_pred_knn = grid_knn.best_estimator_.predict(X_test_scaled)
print("KNN Best Params:", grid_knn.best_params_)
print_metrics(y_test, y_pred_knn, "KNN")

# ---------------------- SVM MODEL ----------------------
svm = SVC()
param_grid = {"C": [0.1, 1, 10], "kernel": ["linear", "rbf"]}
grid_svm = GridSearchCV(svm, param_grid, cv=5, scoring='accuracy')
grid_svm.fit(X_train_scaled, y_train)
y_pred_svm = grid_svm.best_estimator_.predict(X_test_scaled)
print("SVM Best Params:", grid_svm.best_params_)
print_metrics(y_test, y_pred_svm, "SVM")

# ---------------------- LOGISTIC REGRESSION ----------------------
log_reg = LogisticRegression()
param_grid = {"C": [0.1, 1, 10]}
grid_logreg = GridSearchCV(log_reg, param_grid, cv=5, scoring='accuracy')
grid_logreg.fit(X_train_scaled, y_train)
y_pred_logreg = grid_logreg.best_estimator_.predict(X_test_scaled)
print("Logistic Regression Best Params:", grid_logreg.best_params_)
print_metrics(y_test, y_pred_logreg, "Logistic Regression")

# ---------------------- DECISION TREE ----------------------
dt = DecisionTreeClassifier()
param_grid = {"max_depth": [3, 5, 10]}
grid_dt = GridSearchCV(dt, param_grid, cv=5, scoring='accuracy')
grid_dt.fit(X_train, y_train)
y_pred_dt = grid_dt.best_estimator_.predict(X_test)
print("Decision Tree Best Params:", grid_dt.best_params_)
print_metrics(y_test, y_pred_dt, "Decision Tree")

# ---------------------- RANDOM FOREST ----------------------
rf = RandomForestClassifier()
scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')
param_grid = {"n_estimators": [50, 100, 200]}
grid_rf = GridSearchCV(rf, param_grid, cv=5, scoring='accuracy')
grid_rf.fit(X_train, y_train)
y_pred_rf = grid_rf.best_estimator_.predict(X_test)
print("Random Forest Best Params:", grid_rf.best_params_)
print_metrics(y_test, y_pred_rf, "Random Forest")




# ---------------------- NAIVE BAYES ----------------------
nb = GaussianNB()
nb.fit(X_train_scaled, y_train)
y_pred_nb = nb.predict(X_test_scaled)
print_metrics(y_test, y_pred_nb, "Naive Bayes")

# ---------------------- XGBOOST ----------------------
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
param_grid = {"n_estimators": [50, 100, 200]}
grid_xgb = GridSearchCV(xgb, param_grid, cv=5, scoring='accuracy')
grid_xgb.fit(X_train, y_train)
y_pred_xgb = grid_xgb.best_estimator_.predict(X_test)
print("XGBoost Best Params:", grid_xgb.best_params_)
print_metrics(y_test, y_pred_xgb, "XGBoost")

# Plot ROC curves
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves")
plt.legend()
plt.show()
