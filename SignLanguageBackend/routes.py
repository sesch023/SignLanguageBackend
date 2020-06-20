from SignLanguageBackend import app
from flask import request
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
import traceback
from PIL import Image
from flask_cors import cross_origin

model_map = {
    '/api/cnn_5_150_150': app.config["MODELS"]["150x150_5_Layer_CNN.hdf5"]
}


@app.route('/api/cnn_5_150_150', methods=["GET", "POST"])
@cross_origin()
def cnn_5_150_150():
    try:
        print(request.stream['image'])
        image = request.stream['image'].stream
        image_pil = Image.open(image).resize((150, 150)).convert("L")
        image_tf = img_to_array(image_pil).reshape((1, 150, 150, 1))
        prediction = model_map[request.path]["MODEL"].predict(image_tf).tolist()

        classes = model_map[request.path]["CLASSES"]
        prediction_dict = {}

        for class_prediction_index in range(len(prediction[0])):
            if len(classes) > class_prediction_index:
                prediction_dict[classes[class_prediction_index]] = prediction[0][class_prediction_index]
            else:
                prediction_dict[class_prediction_index] = prediction[0][class_prediction_index]

        return prediction_dict, 200
    except Exception as err:
        print(traceback.format_exc())
        return "BAD_REQUEST", 400
