from sanic import Sanic

def create_app():
    app = Sanic()
    
    #register the blueprint
    from ezapi.api import api as api_blueprint
    app.blueprint(api_blueprint)
    return app
    