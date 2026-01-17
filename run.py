import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Get environment configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
