from SignLanguageBackend import app
from flask import request
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
from werkzeug import datastructures
import traceback
from PIL import Image
from flask_restful import Api, Resource, reqparse
from SignLanguageBackend import api

"""

@app.route('/api/cnn_5_150_150', methods=["GET", "POST"])
def cnn_5_150_150():
    try:
        print(request.form)
        print(request.data)
        print(request.args)
        print(request.files)
        image = request.files['image'].stream
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
"""


class SignLanguageCNN(Resource):
    def __init__(self, target_shape, model_config):
        self.model_config = model_config
        self.target_shape = target_shape

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("image", type=datastructures.FileStorage, location='files')
            args = parser.parse_args()
            print(args)
            image = args.image
            image_pil = Image.open(image).resize(self.target_shape).convert("L")
            image_tf = img_to_array(image_pil).reshape((1, 150, 150, 1))
            prediction = self.model_config["MODEL"].predict(image_tf).tolist()

            classes = self.model_config["CLASSES"]
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


api.add_resource(SignLanguageCNN, "/api/cnn_5_150_150",
                 resource_class_kwargs={"target_shape": (150, 150),
                                        "model_config": app.config["MODELS"]["150x150_5_Layer_CNN.hdf5"]})

if __name__ == "__main__":
    app.run(debug=True)