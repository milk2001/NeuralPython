import sys
from matplotlib import pyplot
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator

#funzione che definisce il modello.
def crea_modello():

	model = VGG16(include_top=False, input_shape=(224, 224, 3))
	# rimuovo i layer predefiniti
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


# Funzione che stampa su file le curve di apprendimento
def stampa(history):
	# accuratezza
	pyplot.subplot(212)
	pyplot.title('Accuratezza nella classificazione')
	pyplot.plot(history.history['accuracy'], color='blue', label='train')
	pyplot.plot(history.history['val_accuracy'], color='red', label='test')
	# salvo su file
	filename = sys.argv[0].split('/')[-1]
	pyplot.savefig(filename + '_plotTTED.png')
	pyplot.close()

# addestramento
def addestra():
	# definisco il modello
	model = crea_modello()
	# preparo sia per test che train i batch degli input.
	datagen = ImageDataGenerator(featurewise_center=True)
	# imposto i valori medi RGB del dataset
	#datagen.mean = [123.68, 116.779, 103.939]
	# definisco su quali dati il modello apprenderà e su quali effettuerà i test
	train_it = train_datagen.flow_from_directory('dataset_dogs_vs_cats/train/',
		class_mode='binary', batch_size=64, target_size=(224, 224))
	test_it = test_datagen.flow_from_directory('dataset_dogs_vs_cats/test/',
		class_mode='binary', batch_size=64, target_size=(224, 224))
	# ADDESTRO IL MODELLO
	history = model.fit_generator(train_it, steps_per_epoch=len(train_it),
		validation_data=test_it, validation_steps=len(test_it), epochs=10, verbose=1)
	stampa(history)
	model.save("vgg16.h5")
	#model.save_weights('my_model_weights.h5')

	#calcolo una valutazione sulla precisione del modello appena addestrato
	_, acc = model.evaluate_generator(test_it, steps=len(test_it), verbose=0)
	print('> %.3f' % (acc * 100.0))

addestra()
