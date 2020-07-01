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

api.add_resource(SignLanguageCNN, model_urls["150x150_5_Layer_CNN.hdf5"], endpoint="cnn_5_150_150",
                 resource_class_kwargs={"document_outputs": False,
                                        "target_shape": (150, 150),
                                        "model_config": app.config["MODELS"]["150x150_5_Layer_CNN.hdf5"]})

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

