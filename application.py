import pickle
import os
from flask import Flask, request, render_template, jsonify
import pandas as pd

application = Flask(__name__)
app = application

# Global variable for model
model = None

def load_model():
    """Load the ML model with error handling"""
    global model
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'model.pkl')
        if os.path.exists(model_path):
            model = pickle.load(open(model_path, 'rb'))
            print("✅ Model loaded successfully!")
            return True
        else:
            print("❌ Model file not found at:", model_path)
            return False
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

# Load model on startup
model_loaded = load_model()

@app.route("/")
def index():
    """Homepage route"""
    try:
        return render_template('index.html')
    except Exception as e:
        # Fallback HTML if template is missing
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Forest Fire Prediction System</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #d32f2f; }}
                .status {{ color: #2e7d32; font-weight: bold; }}
                .error {{ color: #d32f2f; }}
                a {{ color: #1976d2; text-decoration: none; padding: 10px 15px; background: #e3f2fd; border-radius: 5px; display: inline-block; margin: 5px; }}
                a:hover {{ background: #bbdefb; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔥 Forest Fire Prediction System</h1>
                <p class="status">✅ Application is running on AWS Elastic Beanstalk</p>
                <p><strong>Model Status:</strong> <span class="{'status' if model_loaded else 'error'}">{'Loaded Successfully' if model_loaded else 'Error Loading Model'}</span></p>
                <p><strong>Framework:</strong> Flask 3.1.3</p>
                <p><strong>Platform:</strong> Python 3.14 on Amazon Linux 2023</p>
                <hr>
                <a href="/predictdata">🔮 Make Prediction</a>
                <a href="/health">🔍 Health Check</a>
                <p><small>Template Error: {str(e)}</small></p>
            </div>
        </body>
        </html>
        '''

@app.route('/predictdata', methods=['GET','POST'])
def predict_datapoint():
    """Prediction route"""
    if request.method == "POST":
        try:
            if not model_loaded or model is None:
                return jsonify({{"error": "Model not loaded properly", "status": "failed"}})
            
            # Get form data
            input_data = {{
                'Temperature': float(request.form.get('Temperature', 0)),
                'RH': float(request.form.get('RH', 0)),
                'Ws': float(request.form.get('Ws', 0)),
                'Rain': float(request.form.get('Rain', 0)),
                'FFMC': float(request.form.get('FFMC', 0)),
                'DMC': float(request.form.get('DMC', 0)),
                'DC': float(request.form.get('DC', 0)),
                'ISI': float(request.form.get('ISI', 0)),
                'BUI': float(request.form.get('BUI', 0)),
                'Classes': float(request.form.get('Classes', 0)),
                'Region': float(request.form.get('Region', 0))
            }}
            
            input_df = pd.DataFrame([input_data])
            result = model.predict(input_df)
            
            try:
                return render_template('home.html', results=round(result[0], 3))
            except:
                return f'''
                <!DOCTYPE html>
                <html>
                <head><title>Prediction Result</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                    .container {{ background: white; padding: 30px; border-radius: 10px; }}
                    .result {{ background: #e8f5e8; padding: 20px; border-radius: 5px; font-size: 24px; text-align: center; }}
                    a {{ color: #1976d2; text-decoration: none; }}
                </style>
                </head>
                <body>
                    <div class="container">
                        <h1>🔥 Forest Fire Prediction Result</h1>
                        <div class="result">
                            <strong>Fire Risk Score: {round(result[0], 3)}</strong>
                        </div>
                        <p><a href="/predictdata">← Make Another Prediction</a></p>
                        <p><a href="/">← Back to Home</a></p>
                    </div>
                </body>
                </html>
                '''
                
        except Exception as e:
            return jsonify({{"error": str(e), "status": "prediction_failed"}})
    
    # GET request - show form
    try:
        return render_template('home.html')
    except:
        # Fallback form
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Forest Fire Prediction Form</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; }
                .form-group { margin: 15px 0; }
                label { display: block; font-weight: bold; margin-bottom: 5px; }
                input[type="number"] { width: 200px; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
                .btn { background: #d32f2f; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                .btn:hover { background: #b71c1c; }
                a { color: #1976d2; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔥 Forest Fire Risk Prediction</h1>
                <p>Enter the environmental parameters to predict fire risk:</p>
                
                <form method="POST">
                    <div class="form-group">
                        <label>Temperature (°C):</label>
                        <input type="number" step="0.01" name="Temperature" placeholder="e.g., 25.5" required>
                    </div>
                    <div class="form-group">
                        <label>Relative Humidity (%):</label>
                        <input type="number" step="0.01" name="RH" placeholder="e.g., 60.0" required>
                    </div>
                    <div class="form-group">
                        <label>Wind Speed (km/h):</label>
                        <input type="number" step="0.01" name="Ws" placeholder="e.g., 5.2" required>
                    </div>
                    <div class="form-group">
                        <label>Rain (mm):</label>
                        <input type="number" step="0.01" name="Rain" placeholder="e.g., 0.0" required>
                    </div>
                    <div class="form-group">
                        <label>FFMC Index:</label>
                        <input type="number" step="0.01" name="FFMC" placeholder="e.g., 85.0" required>
                    </div>
                    <div class="form-group">
                        <label>DMC Index:</label>
                        <input type="number" step="0.01" name="DMC" placeholder="e.g., 15.0" required>
                    </div>
                    <div class="form-group">
                        <label>DC Index:</label>
                        <input type="number" step="0.01" name="DC" placeholder="e.g., 120.0" required>
                    </div>
                    <div class="form-group">
                        <label>ISI Index:</label>
                        <input type="number" step="0.01" name="ISI" placeholder="e.g., 8.5" required>
                    </div>
                    <div class="form-group">
                        <label>BUI Index:</label>
                        <input type="number" step="0.01" name="BUI" placeholder="e.g., 25.0" required>
                    </div>
                    <div class="form-group">
                        <label>Classes:</label>
                        <input type="number" step="0.01" name="Classes" placeholder="e.g., 1.0" required>
                    </div>
                    <div class="form-group">
                        <label>Region:</label>
                        <input type="number" step="0.01" name="Region" placeholder="e.g., 2.0" required>
                    </div>
                    <button type="submit" class="btn">🔮 Predict Fire Risk</button>
                </form>
                
                <p><a href="/">← Back to Home</a></p>
            </div>
        </body>
        </html>
        '''

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "application": "Forest Fire Prediction System",
        "model_loaded": model_loaded,
        "model_status": "loaded" if model_loaded else "error",
        "framework": "Flask 3.1.3",
        "platform": "AWS Elastic Beanstalk",
        "python_version": "3.14",
        "routes": ["/", "/predictdata", "/health"]
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
