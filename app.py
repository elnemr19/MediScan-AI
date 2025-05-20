from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
import os
import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')  # Disable GPU if not needed
tf.keras.backend.set_floatx('float32')  # Enforce consistent precision

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        from auth import User
        return User.get(user_id)
    
    # Root URL redirect
    @app.route('/')
    def root():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    
    # Register blueprints
    from auth import auth_bp
    from views.dashboard import dashboard_bp
    from views.pneumonia import pneumonia_bp
    from views.brain import brain_bp
    from views.sentiment import sentiment_bp
    from views.chatbot import chatbot_bp
    from views.errors import errors_bp
    from views.drugs import drugs_bp


    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(pneumonia_bp)
    app.register_blueprint(brain_bp)
    #app.register_blueprint(sentiment_bp)
    app.register_blueprint(sentiment_bp, url_prefix='/sentiment')
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(drugs_bp, url_prefix='/drugs')
    
    
    # Route debugging
    @app.before_request
    def first_request_handler():
        if not hasattr(app, 'routes_printed'):
            print("\n=== Registered Routes ===")
            for rule in app.url_map.iter_rules():
                print(f"{rule.endpoint}: {rule.methods} {rule.rule}")
            print("========================")
            app.routes_printed = True
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)