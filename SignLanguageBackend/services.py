from SignLanguageBackend import app
from SignLanguageBackend import api
from SignLanguageBackend.SignLanguageCNN import SignLanguageCNN
from SignLanguageBackend.ModelInfo import ModelInfo

model_urls = {
    "150x150_5_Layer_CNN.hdf5": "/cnn_5_150_150",
    "224x224_VGG19_CNN.hdf5": "/vgg19_224_224",
    "224x224_VGG19_CNN_v2.hdf5": "/vgg19_224_224_v2"
}

api.add_resource(ModelInfo, "/model_info", endpoint="model_info", resource_class_kwargs={"model_urls": model_urls})

<<<<<<< HEAD
api.add_resource(SignLanguageCNN, model_urls["150x150_5_Layer_CNN.hdf5"], endpoint="cnn_5_150_150",
                 resource_class_kwargs={"document_outputs": False,
                                        "target_shape": (150, 150),
                                        "model_config": app.config["MODELS"]["150x150_5_Layer_CNN.hdf5"]})
=======
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
>>>>>>> afe3580eba8e757a7609abbc001cb697df19a943

api.add_resource(SignLanguageCNN, model_urls["224x224_VGG19_CNN.hdf5"], endpoint="vgg19_224_224",
                 resource_class_kwargs={"document_outputs": False,
                                        "to_grayscale": False,
                                        "target_shape": (224, 224),
                                        "model_config": app.config["MODELS"]["224x224_VGG19_CNN.hdf5"]})

api.add_resource(SignLanguageCNN, model_urls["224x224_VGG19_CNN_v2.hdf5"], "/default", endpoint="vgg19_224_224_v2",
                 resource_class_kwargs={"document_outputs": False,
                                        "to_grayscale": False,
                                        "target_shape": (224, 224),
                                        "model_config": app.config["MODELS"]["224x224_VGG19_CNN_v2.hdf5"]})

