import numpy as np
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense

max_features = 10000
max_len = 500  # Maximum length of each comment

# Load the data and convert the reviews into integer-encoded sequences
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)

# Combine all data
x_full_train = np.concatenate([x_train, x_test])
y_full_train = np.concatenate([y_train, y_test])

# The first 40,000 records are used as the new training set, and the remaining 10,000 records are used as the new test set.
x_train_new = x_full_train[:40000]
y_train_new = y_full_train[:40000]

x_test_new = x_full_train[40000:]
y_test_new = y_full_train[40000:]

# Pad or truncate the merged data
x_train_new = sequence.pad_sequences(x_train_new, maxlen=max_len)
x_test_new = sequence.pad_sequences(x_test_new, maxlen=max_len)



# Build the RNN model
model = Sequential([
    Embedding(input_dim=max_features, output_dim=32, input_length=max_len),  # Embedding layer
    SimpleRNN(units=32, return_sequences=False),  # Single-layer Simple Recurrent Neural Network
    Dense(units=1, activation='sigmoid')  # Output layer (for binary classification)
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(x_train_new, y_train_new, epochs=5, batch_size=64, validation_split=0.2)

# Evaluate the model
test_loss, test_acc = model.evaluate(x_test_new, y_test_new)
print(f"Test Accuracy: {test_acc:.2f}")

# Save the model for compare and contrast with other models
model.save('rnn_imdb_sentiment_custom.h5')

from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Predict probabilities using the model and convert them to binary classification results
y_pred_probs = model.predict(x_test_new)
y_pred = (y_pred_probs > 0.5).astype(int).flatten()  # Convert probabilities to binary labels

# Generate the confusion matrix
cm = confusion_matrix(y_test_new, y_pred)

# Display the confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Negative', 'Positive'])
disp.plot(cmap='magma')  
plt.title('Confusion Matrix')
plt.show()

# Print the classification report
print("Classification Report:")
report = classification_report(y_test_new, y_pred, target_names=['Negative', 'Positive'])
print(report)
