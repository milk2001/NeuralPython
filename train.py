import sys
from matplotlib import pyplot
from keras.utils import to_categorical
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator

#funzione che definisce il modello.
def define_model():
	model = VGG16(include_top=False, input_shape=(224, 224, 3))
	# setto i layers precaricati come non utilizzabili
	for layer in model.layers:
		layer.trainable = False
	# aggiungo layer per fare classificazione binarie
	flat1 = Flatten()(model.layers[-1].output)
	class1 = Dense(128, activation='relu', kernel_initializer='he_uniform')(flat1)
	output = Dense(1, activation='sigmoid')(class1)
	# ridefinisco il modello con quello modificato
	model = Model(inputs=model.inputs, outputs=output)
	# compilo modello
	opt = SGD(lr=0.001, momentum=0.9)
	model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])
	return model

# addestramento
def train():
	# definisco il modello
	model = define_model()
	# preparo sia per test che train i batch degli input.
	datagen = ImageDataGenerator(featurewise_center=True)
	# valori medi centratura
	#datagen.mean = [123.68, 116.779, 103.939]
	# definisco su quali dati il modello apprenderà e su quali effettuerà i test
	train_it = datagen.flow_from_directory('dataset_dogs_vs_cats/train/',
		class_mode='binary', batch_size=64, target_size=(224, 224))
	test_it = datagen.flow_from_directory('dataset_dogs_vs_cats/test/',
		class_mode='binary', batch_size=64, target_size=(224, 224))
	# ADDESTRO IL MODELLO
	model.fit_generator(train_it, steps_per_epoch=len(train_it),
		validation_data=test_it, validation_steps=len(test_it), epochs=10, verbose=1)
	#salvo
	model.save('vgg16.h5')
	#model.save_weights("pesi.h5")

train()
