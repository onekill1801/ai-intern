# mnist_cnn.py
import tensorflow as tf

# 1. Load dữ liệu MNIST (đã có sẵn trong Keras)
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
# chuẩn hóa và reshape
x_train = x_train.astype("float32") / 255.0
x_test  = x_test.astype("float32") / 255.0
x_train = x_train[..., None]  # shape = (n, 28,28,1)
x_test  = x_test[..., None]

# 2. Build model (một convnet nhỏ)
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(28,28,1)),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# 3. Train
history = model.fit(x_train, y_train, epochs=5, batch_size=64,
                    validation_split=0.1)

# 4. Evaluate
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print("Test accuracy:", test_acc)

# 5. Lưu model
model.save("mnist_cnn.h5")
