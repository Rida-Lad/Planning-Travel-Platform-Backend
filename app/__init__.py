from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    from .routes import cost_calculation,cost_calculation2, bus_options, train_options, plane_options, food, activities, lodging
    app.register_blueprint(cost_calculation.bp)
    app.register_blueprint(cost_calculation2.bp)
    app.register_blueprint(bus_options.travel_bp)
    app.register_blueprint(train_options.travel_bp)
    app.register_blueprint(plane_options.travel_bp)
    app.register_blueprint(food.food_bp)
    app.register_blueprint(activities.activities_bp)
    app.register_blueprint(lodging.lodgings_bp)
    
        
    return app