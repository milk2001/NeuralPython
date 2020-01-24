from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
from keras import models
import numpy as np
import flask
import io
from keras.optimizers import SGD

app = flask.Flask(__name__)
model = None
class_names = ['gatto', 'cane']
def load_model():
	# carico modello pre-trainato
	global model
	model = models.load_model('doggo2cat_model.h5')
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
	return image

@app.route("/", methods=["POST"])
def predict():

	# controllo l'upload della foto
	if flask.request.method == "POST":
		if flask.request.files.get("image"):
			# leggo la foto come PIL
			image = flask.request.files["image"].read()
			image = Image.open(io.BytesIO(image))

			# preprocesso l'immagine
			image = prepare_image(image, target=(200, 200))
			#faccio predizione tramite modello
			preds = int(model.predict(image))
			print(preds)
			#creo un json di risposta con la predizione appena generata
			r = x =  "{ \"animal\": \""+class_names[preds]+"\"}"
			#ritorno il json
	return r

if __name__ == "__main__":
	load_model()
	app.run()
