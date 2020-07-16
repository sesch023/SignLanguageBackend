from SignLanguageBackend import app
from SignLanguageBackend import api
from SignLanguageBackend.SignLanguageCNN import SignLanguageCNN
from SignLanguageBackend.ModelInfo import ModelInfo

# Gültige Urls für Modelle
model_urls = {
    "150x150_5_Layer_CNN.hdf5": "/150x150_cnn_5",
    "224x224_VGG19_CNN.hdf5": "/224x224_vgg19",
    "224x224_VGG19_CNN_v2.hdf5": "/224x224_vgg19_v2",
    "VGG19_Kaggle2.hdf5": "/224x224_vgg19_v3",
    "CNN_Kaggle2.hdf5": "/150x150_cnn_5_v2"
}

# Infos der Modelle mit URLs zurückgeben
api.add_resource(ModelInfo, "/model_info", endpoint="model_info", resource_class_kwargs={"model_urls": model_urls})

# Eigenes Modell mit Eingangsgröße 150x150 und 5 CNN Layern.
api.add_resource(SignLanguageCNN, model_urls["150x150_5_Layer_CNN.hdf5"], endpoint="150x150_cnn_5",
                 resource_class_kwargs={"document_outputs": False,
                                        "target_shape": (150, 150),
                                        "model_config": app.config["MODELS"]["150x150_5_Layer_CNN.hdf5"]})

# VGG19 mit Eingangsgröße 224x224 umtrainiert.
api.add_resource(SignLanguageCNN, model_urls["224x224_VGG19_CNN.hdf5"], endpoint="224x224_vgg19",
                 resource_class_kwargs={"document_outputs": False,
                                        "to_grayscale": False,
                                        "target_shape": (224, 224),
                                        "model_config": app.config["MODELS"]["224x224_VGG19_CNN.hdf5"]})

# VGG19 mit Eingangsgröße 224x224 umtrainiert und mit VGG19_Preprozess der Bilder.
api.add_resource(SignLanguageCNN, model_urls["224x224_VGG19_CNN_v2.hdf5"], endpoint="224x224_vgg19_v2",
                 resource_class_kwargs={"document_outputs": False,
                                        "to_grayscale": False,
                                        "target_shape": (224, 224),
                                        "model_config": app.config["MODELS"]["224x224_VGG19_CNN_v2.hdf5"]})

# VGG19 mit Eingangsgröße 224x224 umtrainiert, mit VGG19_Preprozess der Bilder und
# deaktivierten Basemodeltraining. Bekannt aus Ausarbeitung.
api.add_resource(SignLanguageCNN, model_urls["VGG19_Kaggle2.hdf5"], "/default", endpoint="224x224_vgg19_v3",
                 resource_class_kwargs={"document_outputs": False,
                                        "to_grayscale": False,
                                        "target_shape": (224, 224),
                                        "model_config": app.config["MODELS"]["VGG19_Kaggle2.hdf5"]})

# CNN bekannt aus Ausarbeitung für den ASL-Alphabet Datensatz.
api.add_resource(SignLanguageCNN, model_urls["CNN_Kaggle2.hdf5"], endpoint="150x150_cnn_5_v2",
                 resource_class_kwargs={"document_outputs": False,
                                        "to_grayscale": True,
                                        "target_shape": (200, 200),
                                        "model_config": app.config["MODELS"]["CNN_Kaggle2.hdf5"]})
