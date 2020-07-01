from flask_restful import Resource


class ModelInfo(Resource):
    def __init__(self, model_urls):
        self.model_urls = model_urls

    def get(self):
        return self.model_urls, 200
