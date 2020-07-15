from flask_restful import Resource


class ModelInfo(Resource):
    """
    Resource, die URL Infos zu den Modellen zurückgibt.
    """
    def __init__(self, model_urls):
        """
        Resource, die URL Infos zu den Modellen zurückgibt.
        :param model_urls: URL Infos, die zurückgegeben werden.
        """
        self.model_urls = model_urls

    def get(self):
        """
        Gibt die Model Infos mittels get-Request zurück.
        """
        return self.model_urls, 200
