from flask import Flask, request, render_template_string, jsonify
import os

# CRITICAL: Must be named 'application' for Elastic Beanstalk
application = Flask(__name__)

@application.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Forest Fire Prediction System</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 40px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                background: white; 
                padding: 40px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                max-width: 800px;
                margin: 0 auto;
            }
            h1 { 
                color: #d32f2f; 
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            .status-card {
                background: #e8f5e8;
                border-left: 5px solid #4caf50;
                padding: 20px;
                margin: 20px 0;
                border-radius: 5px;
            }
            .info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .info-item {
                background: #f5f5f5;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }
            .btn {
                display: inline-block;
                background: #1976d2;
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 8px;
                margin: 10px;
                transition: background 0.3s;
            }
            .btn:hover { background: #1565c0; }
            .btn-success { background: #4caf50; }
            .btn-success:hover { background: #45a049; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔥 Forest Fire Prediction System</h1>
            
            <div class="status-card">
                <h3>✅ System Status: ONLINE</h3>
                <p>Your ML-powered Forest Fire Risk Assessment System is running successfully on AWS!</p>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <strong>Platform</strong><br>
                    AWS Elastic Beanstalk
                </div>
                <div class="info-item">
                    <strong>Framework</strong><br>
                    Flask 3.1.3
                </div>
                <div class="info-item">
                    <strong>Python</strong><br>
                    3.14 (Latest)
                </div>
                <div class="info-item">
                    <strong>OS</strong><br>
                    Amazon Linux 2023
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 40px;">
                <a href="/health" class="btn">🔍 Health Check</a>
                <a href="/predict" class="btn btn-success">🔮 Start Prediction</a>
            </div>
        </div>
    </body>
    </html>
    """)

@application.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "Forest Fire ML System is running successfully",
        "platform": "AWS Elastic Beanstalk",
        "framework": "Flask 3.1.3",
        "python_version": "3.14",
        "os": "Amazon Linux 2023",
        "environment": "production",
        "timestamp": "2026-03-03T12:42:06Z"
    })

@application.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get form data
        try:
            data = {
                'temperature': float(request.form.get('temperature', 0)),
                'humidity': float(request.form.get('humidity', 0)),
                'wind_speed': float(request.form.get('wind_speed', 0)),
                'rainfall': float(request.form.get('rainfall', 0))
            }
            
            # Simple prediction logic (replace with your ML model)
            risk_score = (data['temperature'] * 0.3 + 
                         (100 - data['humidity']) * 0.4 + 
                         data['wind_speed'] * 0.2 + 
                         (10 - data['rainfall']) * 0.1) / 10
            
            risk_level = "Low" if risk_score < 3 else "Medium" if risk_score < 7 else "High"
            
            return render_template_string("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Prediction Result</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                    .container { background: white; padding: 40px; border-radius: 15px; max-width: 600px; margin: 0 auto; }
                    .result { background: #e3f2fd; padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0; }
                    .risk-score { font-size: 3em; font-weight: bold; color: #1976d2; }
                    .risk-level { font-size: 1.5em; margin: 10px 0; }
                    .btn { background: #1976d2; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔥 Fire Risk Assessment Result</h1>
                    <div class="result">
                        <div class="risk-score">{{ "%.1f"|format(risk_score) }}</div>
                        <div class="risk-level">Risk Level: <strong>{{ risk_level }}</strong></div>
                        <p>Based on current environmental conditions</p>
                    </div>
                    <p><a href="/predict" class="btn">← New Prediction</a> <a href="/" class="btn">🏠 Home</a></p>
                </div>
            </body>
            </html>
            """, risk_score=risk_score, risk_level=risk_level)
            
        except Exception as e:
            return f"Error processing prediction: {str(e)}"
    
    # GET request - show form
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Forest Fire Risk Prediction</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 40px; border-radius: 15px; max-width: 600px; margin: 0 auto; }
            .form-group { margin: 20px 0; }
            label { display: block; font-weight: bold; margin-bottom: 8px; color: #333; }
            input[type="number"] { 
                width: 100%; 
                padding: 12px; 
                border: 2px solid #ddd; 
                border-radius: 8px; 
                font-size: 16px;
                box-sizing: border-box;
            }
            input[type="number"]:focus { border-color: #1976d2; outline: none; }
            .btn { 
                background: #d32f2f; 
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                font-size: 18px;
                width: 100%;
                margin-top: 20px;
            }
            .btn:hover { background: #b71c1c; }
            .info { background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔥 Forest Fire Risk Prediction</h1>
            
            <div class="info">
                <strong>📊 Enter Environmental Data:</strong><br>
                Provide current weather conditions to assess fire risk in your area.
            </div>
            
            <form method="POST">
                <div class="form-group">
                    <label for="temperature">🌡️ Temperature (°C):</label>
                    <input type="number" id="temperature" name="temperature" step="0.1" min="-50" max="60" placeholder="e.g., 25.5" required>
                </div>
                
                <div class="form-group">
                    <label for="humidity">💧 Relative Humidity (%):</label>
                    <input type="number" id="humidity" name="humidity" step="0.1" min="0" max="100" placeholder="e.g., 45.0" required>
                </div>
                
                <div class="form-group">
                    <label for="wind_speed">💨 Wind Speed (km/h):</label>
                    <input type="number" id="wind_speed" name="wind_speed" step="0.1" min="0" max="200" placeholder="e.g., 15.2" required>
                </div>
                
                <div class="form-group">
                    <label for="rainfall">🌧️ Rainfall (mm):</label>
                    <input type="number" id="rainfall" name="rainfall" step="0.1" min="0" max="500" placeholder="e.g., 0.0" required>
                </div>
                
                <button type="submit" class="btn">🔮 Predict Fire Risk</button>
            </form>
            
            <p style="text-align: center; margin-top: 30px;">
                <a href="/" style="color: #1976d2; text-decoration: none;">← Back to Home</a>
            </p>
        </div>
    </body>
    </html>
    """)

# CRITICAL: For Elastic Beanstalk, don't include if __name__ == "__main__"
# The WSGI server (Gunicorn) will import this module directly
