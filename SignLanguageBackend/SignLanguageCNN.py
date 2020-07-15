from tensorflow.keras.preprocessing.image import img_to_array
from werkzeug import datastructures
import traceback
from PIL import Image
from flask_restful import Resource, reqparse
import base64
from io import BytesIO
import datetime


class SignLanguageCNN(Resource):
    """
    Resource für das Bereitstellen eines Tensorflow / Keras Modells über das Web.
    """

    def __init__(self, target_shape, model_config, to_grayscale=True, document_outputs=False):
        """
        Resource für das Bereitstellen eines Tensorflow / Keras Modells über das Web.
        :param target_shape: Die Zielgröße eines gesendeten Bildes vor dem Klassifikationsvorgang.
        :param model_config: Ein Element einer der in der Intialisierung erstellten ModellConfigs.
        :param to_grayscale: Verarbeitet das CNN Grauwerte oder RGB Werte?
        :param document_outputs: Schreibe die erhaltenen Bilder für Debug-Zwecke mit Klassifikation in
                                 das Out-Verzeichnis.
        """
        self.model_config = model_config
        self.target_shape = target_shape
        self.to_grayscale = to_grayscale
        self.document_outputs = document_outputs

    def post(self):
        """
        Post Request mit Bild per FileStorage oder Base64-Post-Variable auf ein hinterlegtes Modell. Gibt
        eine Prediction als Dictionary zu jeder Klasse vom Modell zurück. Dieses ist auch mit einem
        BEST_KEY hinterlegt, welche die relevanteste Class-Prediction liefert.
        :return: Prediction Dictionary, mit den Modellergebnissen.
        """
        try:
            # Parse den Request
            parser = reqparse.RequestParser()
            parser.add_argument("image", type=datastructures.FileStorage, location='files')
            parser.add_argument("image_base_64")
            args = parser.parse_args()

            # Image per FileStorage im Request
            if args.image:
                image = args.image
            # Image per Base64 in Post
            else:
                image = BytesIO(base64.b64decode(args.image_base_64))

            # Öffne das Bild und resize es.
            image_pil = Image.open(image).resize(self.target_shape)
            color_dim = 3

            # Wenn Grauwert ausgewertet
            if self.to_grayscale:
                image_pil = image_pil.convert("L")
                color_dim = 1
            # Wenn RGB ausgewertet
            else:
                image_pil = image_pil.convert("RGB")

            # Image in ein Tensorflow Array, Reshape es in 4 Dimensionen (BatchSize (1), Breite, Höhe, Farben)
            image_tf = img_to_array(image_pil).reshape((1, self.target_shape[0], self.target_shape[1], color_dim))
            # Prediction für das Bild, mit der genutzten Config.
            prediction = self.model_config["MODEL"].predict(image_tf).tolist()

            # Bereite Dictionary für Auswertung vor.
            classes = self.model_config["CLASSES"]
            prediction_dict = {}
            max_val = 0.0
            max_key = None

            # Für alle Predictions
            for class_prediction_index in range(len(prediction[0])):
                # Nutze hinterlegten beschreibenden Key, wenn in hinterlegten Classes vorhanden
                if len(classes) > class_prediction_index:
                    key = classes[class_prediction_index]
                # Nutze den Index Key der Vorhersage
                else:
                    key = class_prediction_index

                # Hinterlege Prediction-Value hinter beschreibenden Key
                prediction_dict[key] = prediction[0][class_prediction_index]

                # Suche Besten Key
                if prediction_dict[key] > max_val:
                    max_key = key
                    max_val = prediction_dict[key]

            # Hinterlegen des besten Ergebnis
            prediction_dict["BEST_KEY"] = max_key

            # Wenn Dokumente ausgegeben werden sollen
            if self.document_outputs:
                now = datetime.datetime.now()
                image_pil.save("out/" + now.strftime("%m_%d_%Y_%H_%M_%S") + "_" + prediction_dict["BEST_KEY"] + ".jpg")

            return prediction_dict, 200
        except Exception:
            print(traceback.format_exc())
            return "BAD REQUEST", 400