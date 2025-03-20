# app.py (Entry Point)
from app import create_app
from flask_cors import CORS

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

    # Enable CORS for all routes
    CORS(app, supports_credentials=True)