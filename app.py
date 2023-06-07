from flask import Flask, render_template, request
import os

from keras_preprocessing.image import load_img
from keras_preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
# from keras.preprocessing.image import load_img,img_to_array
import numpy as np
import cv2
#from tensorflow.keras.preprocessing.image import load_img,img_to_array
app = Flask(__name__, static_folder='static')
dic = {0 : 'Blight', 1 : 'Gray_Leaf_Spot',2: 'Healthy', 3:'Common_Rust' , 4:'None'}

model = load_model('model6.h5')

# model.make_predict_function()

def predict_label(img_path):
    i=load_img(img_path, target_size = (128, 128))
    i=img_to_array(i)/255 
    i=np.expand_dims(i, axis = 0) 
    
    p = model.predict(i)
    p = np.argmax(np.round(p),axis=1)
    return dic[p[0]]
    


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("newpage.html")

@app.route("/camera", methods=['GET', 'POST'])
def camera():
	return render_template("result.html")

@app.route('/choosefile')
def home():
    return render_template('index.html')

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)

	return render_template("index.html", prediction = p, img_path = img_path)


import cv2
@app.route("/captureimage",methods = ['GET','POST'])
def live_camera():
      return render_template("result.html")
    
# Call the function to capture the image

def capture_image():
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Could not open webcam")
        return

    # Read the image from the webcam
    ret, frame = cap.read()

    # Check if the frame was read correctly
    if not ret:
        print("Failed to capture image")
        return

    # Save the captured image
    cv2.imwrite("static/captured_image.jpg", frame)
    img_path = "static/" + "captured_image.jpg"
    # Release the webcam
    cap.release()

    print("Image captured successfully")


@app.route('/process_image', methods=['POST'])
def process_image():
      image_file = request.files['image_file']
      print("image loaded successfully")
    # Save the image file or perform further processing as needed
      image_file.save('static/captured_image.jpg')
      img_path = "static/captured_image.jpg"
      p = predict_label(img_path)
      return {"predicted":p}


def pred_corn_dis(corn_plant):
  test_image = load_img(corn_plant, target_size = (128, 128)) 
  
  
  test_image = img_to_array(test_image)/255 
  test_image = np.expand_dims(test_image, axis = 0) 
  
  result = model.predict(test_image) 
  
  
  pred = np.argmax(result, axis=1)
  print(pred)
  if pred==0:
      return "Blight", 'corn-Blight.html'
       
  elif pred==1:
      return "Gray_Leaf_Spot", 'Corn_leafspot.html'
        
  elif pred==2:
      return "Healthy", 'Corn_Healthy.html'
        
  elif pred==3:
      return "Common_Rust", 'Corn_Rust.html'
  else :
      return "Enter valid images", 'Corn_Rust - Copy.html'

      

@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] 
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join("C:/Users/ramac/PycharmProjects/ICLDCCNN/static/upload", filename)
        file.save(file_path)

        print("@@ Predicting class......")
        pred, output_page = pred_corn_dis(corn_plant=file_path)
              
        return render_template(output_page, pred_output = pred, user_image = file_path)
 





if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)
