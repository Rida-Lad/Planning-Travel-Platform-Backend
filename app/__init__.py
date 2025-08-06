from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    from .routes import cost_calculation,cost_calculation2, bus_options
    app.register_blueprint(cost_calculation.bp)
    app.register_blueprint(cost_calculation2.bp)
    app.register_blueprint(bus_options.travel_bp)
    
        
    return app