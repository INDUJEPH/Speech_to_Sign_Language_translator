import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense

# 1️⃣ Define a Simple Neural Network Model
def create_model():
    model = Sequential([
        Dense(64, activation='relu', input_shape=(10,)),  # Input layer with 10 features
        Dense(32, activation='relu'),  # Hidden layer
        Dense(1, activation='sigmoid')  # Output layer (for binary classification)
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


# 2️⃣ Generate Dummy Training Data
X_train = np.random.rand(100, 10)  # 100 samples, 10 features each
y_train = np.random.randint(0, 2, 100)  # Binary labels (0 or 1)

# 3️⃣ Create and Train the Model
model = create_model()
model.summary()  # Print model architecture

print("\nTraining the model...\n")
model.fit(X_train, y_train, epochs=10, batch_size=8)

# 4️⃣ Save the Model as 'model.h5'
model.save('model.h5')
print("\n✅ Model saved successfully as 'model.h5'")

# 5️⃣ Load the Model to Verify
print("\nLoading the saved model...\n")
loaded_model = load_model('model.h5')
loaded_model.summary()  # Print model summary to verify
