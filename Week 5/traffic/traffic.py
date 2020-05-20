import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import timeit

from sklearn.model_selection import train_test_split

EPOCHS = 5
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")
    
    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # t = timeit.Timer("images, labels = load_data(sys.argv[1])", "from __main__ import load_data")
    # print(t.timeit(number=1))

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    model.summary()

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # Declare image & labels list - We later convert the images list into an np array - No we don't!
    # We return a list of NP Arrays!
    # Also we will not label each group of images but EACH image 
    images = []
    labels = []

    # Iterate through each category in directory
    for category_folder in os.listdir(data_dir):
        # Skip .DS_File
        if category_folder.startswith("."):
            continue

        # Get the path to each category's folder
        image_folder = os.path.join(data_dir, category_folder)

        # Iterate through the directory of each label
        for ppm_file in os.listdir(image_folder):
            # Extract the ppm file and resize it - No need to focus on the 3 channels here, since imread takes them by default 
            raw_ppm = cv2.imread(os.path.join(image_folder, ppm_file))
            resized_ppm = cv2.resize(raw_ppm, dsize=(IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_AREA)
            # Append image & label
            images.append(resized_ppm)
            labels.append(category_folder)

    # Return a tuple w/ list of images & list of labels (->43*amount of images per folder labels)
    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    model = tf.keras.models.Sequential([
        
        # First Convoluational layer to create 32 feature maps with a kernel size of 3,3 (More fm's gave me worse accuracy)
        tf.keras.layers.Conv2D(32, (3,3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3), use_bias=True),

    

        # Pool by selecting highest values from 2x2 matrix
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        # Flatten into single dimension
        tf.keras.layers.Flatten(),

        # First Dropout
        tf.keras.layers.Dropout(0.3),

        # Create dense NN - 1 hidden layer is generally enough
        tf.keras.layers.Dense(129, activation="relu"),

        # Second Dropout
        tf.keras.layers.Dropout(0.03),

        # Create Output layer
        tf.keras.layers.Dense(43, activation="softmax")

        ])

    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])


    return model


if __name__ == "__main__":
    main()
