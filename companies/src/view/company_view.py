from flask_restful import Resource


class VistaPing(Resource): 
    def get(self):
        return "Pong"

