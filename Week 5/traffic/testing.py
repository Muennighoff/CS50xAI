import cv2
import numpy as np
import tensorflow as tf

IMG_WIDTH = 30
IMG_HEIGHT = 30

new_model = tf.keras.models.load_model('trained2')

# Check its architecture
new_model.summary()

# To get the fourth array value you can either declare a list like in traffic.py and append it
# or simply extend the dimension
# images = []
# images.append(test_image)
# x = np.array(images)

test_image_raw = cv2.imread("test_image/test6.png")
test_image = cv2.resize(test_image_raw, dsize=(IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_AREA)
test_image = np.expand_dims(test_image, axis=0)

prediction = new_model.predict(test_image)[0]

winner = list(prediction).index(max(prediction))


print(prediction)
print("WINNER: ", winner)