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

#carico modello
model = models.load_model('vgg16.h5')
opt = SGD(lr=0.001, momentum=0.9)
model.compile(loss='binary_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])
#model.summary()

test = None #frame che sarà utilizzato per il motion detection
video = VideoStream(src=0).start() #flusso webcam
time.sleep(2.0)
cane = 0
gatto = 0
a = 1
color1 = 0
color2 = 0

while True:
	frame = video.read()
	if frame is None:
		break

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	if test is None:
		test = gray
		continue
    #generazione di due frame per il rilevamento del movimento
	frameDelta = cv2.absdiff(test, gray)
    #frame di soglia
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	a = a+1
	for c in cnts:
    	# se l'area è minore vuol dire che non c'è movimento
		if cv2.contourArea(c) < 800:
				continue

    	# altrimenti disegno il rettangolo dove ho notato cambiamenti
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #trasformo il frame in RGB
		im = Image.fromarray(frame, 'RGB')
        #Ridimensionamento della foto per darla in pasto al modello
		im = im.resize((224,224))
		img_array = np.array(im)
		img_array = np.expand_dims(img_array, axis=0)
		img_array = img_array - [123.68, 116.779, 103.939]
        #faccio predizione tramite modello
		if a%30==0: #1 volta al sec
			prediction = model.predict(img_array)
			#scrivo sul frame la predizione
			cane = round(prediction[0][0]*100,2)
			gatto = round(abs(cane-100), 2)

			if cane>50:
				color1 = 255
				color2 = 0
			else:
				color1 = 0
				color2 = 255

		cv2.putText(frame,"cane:  "+str(cane)+"%", (480,30),cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,color1,color2),2)
		cv2.putText(frame,"gatto: "+str(gatto)+"%",(480,50),cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,color2,color1),2)
	cv2.imshow("output", frame)
	cv2.imshow("soglia", thresh)
	cv2.imshow("deltaOutput", frameDelta)
	key=cv2.waitKey(1)
	if key == ord('q'): #per uscire
		break
	if key == ord('x'): #utile per aggiornare il frame di riferimento per il motion detection
		test = None
video.stop()
cv2.destroyAllWindows()
