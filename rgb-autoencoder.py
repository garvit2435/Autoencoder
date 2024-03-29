from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Conv3D, MaxPooling3D
from keras.models import Model
from keras.datasets import mnist
from keras.callbacks import TensorBoard
from keras import backend as K
import numpy as np
import matplotlib.pyplot as plt
import pickle
from google.colab import drive
from keras.datasets import cifar10
import cv2

#drive.mount("/content/drive", force_remount=True)
#with open("/content/drive/My Drive/Colab Notebooks/cifar-10-python.tar.gz","rb") as file:
#  images_array = pickle.load(file)

#images_array = np.array(images_array)
#print(images_array.shape)

(X_train, y_train), (X_test, y_test) = cifar10.load_data()

#training_set = images_array[:10000,:].astype('float32')
#training_set = training_set/255
#test_set = images_array[10000:14000,:].astype('float32')
#test_set = test_set/255
#print(training_set.shape)
#print(test_set.shape)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

input_img = Input(shape=(32, 32, 3))
print(input_img)

x = Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)

encoded = MaxPooling2D((2, 2), padding='same')(x)
print(encoded)

x = Conv2D(8, (3, 3), activation='relu', padding='same')(encoded)
x = UpSampling2D((2, 2))(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)

decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

encoder= Model(input_img, encoded)
decoder= Model(encoded, decoded)

autoencoder = Model(input_img, decoded)

autoencoder.summary()

#tbCallBack =TensorBoard(log_dir='./log', histogram_freq=1,write_graph=True,write_grads=True,batch_size=32,write_images=True)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
autoencoder.fit(X_train, X_train, epochs=40, batch_size=64, shuffle=True, validation_data=(X_test, X_test), verbose=1)
autoencoder.save('/content/drive/My Drive/encoder_decoder.h5',include_optimizer=True)

decoded_imgs = autoencoder.predict(X_test)
decoded_imgs.shape
n = 10
plt.figure(figsize=(20, 8))
for i in range(n): # display original
  ax = plt.subplot(2, n, i + 1)
  plt.imshow(X_test[i])
  plt.gray()
  ax.set_axis_off() # display reconstruction
  ax = plt.subplot(2, n, i + n + 1)
  plt.imshow(decoded_imgs[i])
  plt.gray()
  ax.set_axis_off()
plt.show()

# take a look at the 128-dimensional encoded representation
encoder = Model(input_img, encoded)
encoded_imgs = encoder.predict(X_test)
print(encoded_imgs.shape)
n = 10
plt.figure(figsize=(10, 4), dpi=100)
for i in range(n):
  ax = plt.subplot(1, n, i + 1)
  plt.imshow(encoded_imgs[i].reshape(8,16).T)
  plt.gray()
  ax.set_axis_off()
  plt.show()
encoder.save('/content/drive/My Drive/encoder.h5')

# save latent space features 32-d vector
pickle.dump(encoded_imgs, open('/content/drive/My Drive/conv_autoe_features.pickle', 'wb'))
