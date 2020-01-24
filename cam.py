from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
from PIL import Image
from keras import models
from keras.optimizers import SGD

class_names = ['gatto', 'cane']
#Load the saved model
model = models.load_model('doggo2cat_model.h5')
opt = SGD(lr=0.001, momentum=0.9)
model.compile(loss='binary_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])
#model.summary()

test = None #frame che sarà utilizzato per il motion detection
video = VideoStream(src=0).start() #flusso webcam
time.sleep(2.0)

while True:
	frame = video.read()
	if frame is None:
		break

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	if test is None:
		test = gray
		continue
    #generazione di due frame per la detenzione del movimento
	frameDelta = cv2.absdiff(test, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	for c in cnts:
    	# se l'area è minore vuol dire che non c'è movimento
		if cv2.contourArea(c) < 500:
				continue

    	# altrimenti disegno il rettangolo dove ho notato cambiamenti
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #trasformo il frame in RGB
		im = Image.fromarray(frame, 'RGB')
        #Ridimensionamento della foto per darla in pasto al modello
		im = im.resize((200,200))
		img_array = np.array(im)
		img_array = np.expand_dims(img_array, axis=0)
        #faccio predizione tramite modello
		prediction = int(model.predict(img_array))
        #scrivo sul frame la predizione
		cv2.putText(frame,class_names[prediction], (500,50),cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,255),2)

	cv2.imshow("doggo", frame)
	cv2.imshow("traccia", thresh)
	cv2.imshow("delta", frameDelta)
	key=cv2.waitKey(1)
	if key == ord('q'): #per uscire
		break
	if key == ord('x'): #utile per aggiornare il frame di riferimento per il motion detection
		test = None
video.stop()
cv2.destroyAllWindows()
