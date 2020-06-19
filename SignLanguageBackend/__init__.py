from config import Config
from tensorflow.keras.models import load_model
from tensorflow.keras.backend import backend
import keras
import glob
import os
from flask_api import FlaskAPI

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
app = FlaskAPI(__name__)
app.config.from_object(Config)

app.config["MODELS"] = {}

for model in glob.glob(app.config["MODEL_FOLDER_PATH"] + "*.hdf5"):
    print("Loading Model: " + model)
    model_loaded = load_model(model)
    app.config["MODELS"][os.path.basename(model)] = {
        "MODEL_NAME": os.path.basename(model),
        "MODEL": model_loaded,
        "CLASSES": []
    }

    class_file = model + ".classes"
    if os.path.exists(class_file):
        with open(class_file) as file:
            content = file.read()
            for line in content.splitlines():
                app.config["MODELS"][os.path.basename(model)]["CLASSES"].append(line)


from SignLanguageBackend import routes
