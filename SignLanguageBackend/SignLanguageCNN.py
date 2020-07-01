from tensorflow.keras.preprocessing.image import img_to_array
from werkzeug import datastructures
import traceback
from PIL import Image
from flask_restful import Resource, reqparse
import base64
from io import BytesIO
import datetime


class SignLanguageCNN(Resource):
    def __init__(self, target_shape, model_config, to_grayscale=True, document_outputs=False):
        self.model_config = model_config
        self.target_shape = target_shape
        self.to_grayscale = to_grayscale
        self.document_outputs = document_outputs

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

            image_pil = Image.open(image).resize(self.target_shape)
            color_dim = 3

            if self.to_grayscale:
                image_pil = image_pil.convert("L")
                color_dim = 1
            else:
                image_pil = image_pil.convert("RGB")

            image_tf = img_to_array(image_pil).reshape((1, self.target_shape[0], self.target_shape[1], color_dim))
            prediction = self.model_config["MODEL"].predict(image_tf).tolist()

            classes = self.model_config["CLASSES"]
            prediction_dict = {}
            max_val = 0.0
            max_key = None

            for class_prediction_index in range(len(prediction[0])):
                if len(classes) > class_prediction_index:
                    key = classes[class_prediction_index]
                else:
                    key = class_prediction_index

                prediction_dict[key] = prediction[0][class_prediction_index]

                if prediction_dict[key] > max_val:
                    max_key = key
                    max_val = prediction_dict[key]

            prediction_dict["BEST_KEY"] = max_key

            if self.document_outputs:
                now = datetime.datetime.now()
                image_pil.save("out/" + now.strftime("%m_%d_%Y_%H_%M_%S") + "_" + prediction_dict["BEST_KEY"] + ".jpg")

            return prediction_dict, 200
        except Exception:
            print(traceback.format_exc())
            return "BAD REQUEST", 400