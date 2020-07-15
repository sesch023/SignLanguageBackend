import os

# CPU nutzen
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from config import Config
from tensorflow.keras.models import load_model
import glob
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import tensorflow as tf

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
app = Flask(__name__)
# Cors erlauben
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
app.config.from_object(Config)

app.config["MODELS"] = {}

# Modelle im in Config hinterlegten MODEL_FOLDER_PATH laden.
for model in glob.glob(app.config["MODEL_FOLDER_PATH"] + "*.hdf5"):
    print("Loading Model: " + model)
    # Model mit CPU laden
    with tf.device('/cpu:0'):
        model_loaded = load_model(model)
    # Model Config hinterlegen
    app.config["MODELS"][os.path.basename(model)] = {
        # Name des Modells
        "MODEL_NAME": os.path.basename(model),
        # Das Modell
        "MODEL": model_loaded,
        # Zurückgegebene Classes des Modells
        "CLASSES": []
    }

    # Klassenbeschreibung lesen, wenn hinterlegt
    class_file = model + ".classes"
    if os.path.exists(class_file):
        with open(class_file) as file:
            content = file.read()
            for line in content.splitlines():
                app.config["MODELS"][os.path.basename(model)]["CLASSES"].append(line)


from SignLanguageBackend import services
