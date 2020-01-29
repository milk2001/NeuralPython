from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
from keras import models
import numpy as np
import flask
import io
from keras.optimizers import SGD
import json

app = flask.Flask(__name__)
model = None
def load_model():
	# carico modello pre-trainato
	global model
	model = models.load_model('vgg16.h5')
	opt = SGD(lr=0.001, momentum=0.9)
	model.compile(loss='binary_crossentropy',
	              optimizer=opt,
	              metrics=['accuracy'])

def prepare_image(image, target):
	# nel remoto caso in cui l'immagine di input non sia rgb, la converto
	if image.mode != "RGB":
		image = image.convert("RGB")
	# ridimensiono l'immagine per il modello
	image = image.resize(target)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	#image = image - [123.68, 116.779, 103.939]
	return image

@app.route("/", methods=["POST"])
def predict():
	data = {}
	# controllo l'upload della foto
	if flask.request.method == "POST":
		if flask.request.files.get("image"):
			# leggo la foto come PIL
			image = flask.request.files["image"].read()
			image = Image.open(io.BytesIO(image))

			# preprocesso l'immagine
			image = prepare_image(image, target=(224, 224))
			#faccio predizione tramite modello
			preds = model.predict(image)
			#creo un json di risposta con la predizione appena generata"
			data['dog'] = round(preds[0][0]*100,2)
			data['cat']= round(abs(data['dog']-100), 2)
			if data['dog']>50:
				data['animal'] = "dog"
			else:
				data['animal'] = "cat"
			#ritorno il "json"
			print(data)
	return json.dumps(data)

if __name__ == "__main__":
	load_model()
	app.run()
