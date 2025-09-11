import joblib
import numpy as np

# Load lại model đã lưu
saved = joblib.load("iris_knn.joblib")
model = saved['model']
scaler = saved['scaler']

# Ví dụ dữ liệu mới: [sepal length, sepal width, petal length, petal width]
X_new = np.array([[5.1, 3.5, 1.4, 0.2]])
X_new_scaled = scaler.transform(X_new)

y_pred = model.predict(X_new_scaled)
print("Kết quả dự đoán:", y_pred)
