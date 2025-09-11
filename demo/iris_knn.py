# iris_knn.py
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib  # để lưu model

# 1. Load dữ liệu
iris = load_iris()
X, y = iris.data, iris.target
print("Shape X, y:", X.shape, y.shape)

# 2. Chia dữ liệu
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Tiền xử lý: chuẩn hóa (rất quan trọng với KNN)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# 4. Tạo mô hình KNN và huấn luyện
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train_s, y_train)

# 5. Đánh giá
y_pred = model.predict(X_test_s)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification report:\n", classification_report(y_test, y_pred))

# 6. Cross-validation (baseline)
scores = cross_val_score(model, scaler.transform(X), y, cv=5)
print("Cross-val scores:", scores, "Mean:", scores.mean())

# 7. Lưu model + scaler
joblib.dump({'model': model, 'scaler': scaler}, "iris_knn.joblib")
