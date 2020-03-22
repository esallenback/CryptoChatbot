import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import requests
requests.packages.urllib3.disable_warnings()
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

data = tf.keras.datasets.mnist  #28 by 28 images of hand written digits

(x, y), (xTest, yTest) = data.load_data()
x = tf.keras.utils.normalize(x, axis=1)
xTest = tf.keras.utils.normalize(xTest, axis=1)

print(x[0])
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x, y, epochs=3)
#model.save('deep learn tutorial')
pred = model.predict([xTest])
print(pred)
print(np.argmax(pred[0]))
plt.imshow(xTest[0])
plt.show()