from SignLanguageBackend import app
from tensorflow.keras.preprocessing.image import img_to_array
from werkzeug import datastructures
import traceback
from PIL import Image
from flask_restful import Resource, reqparse
from flask import request
from SignLanguageBackend import api
import base64
from io import BytesIO


class SignLanguageCNN(Resource):
    def __init__(self, target_shape, model_config):
        self.model_config = model_config
        self.target_shape = target_shape

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("image", type=datastructures.FileStorage, location='files')
            parser.add_argument("image_base_64")
            args = parser.parse_args()

            if args.image:
                image = args.image
            else:
                image = BytesIO(base64.b64decode(args.image_base_64))

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
        except Exception:
            print(traceback.format_exc())
            return "BAD REQUEST", 400


api.add_resource(SignLanguageCNN, "/cnn_5_150_150",
                 resource_class_kwargs={"target_shape": (150, 150),
                                        "model_config": app.config["MODELS"]["150x150_5_Layer_CNN.hdf5"]})
