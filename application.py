from flask import Flask

application = Flask(__name__)

@application.route("/")
def home():
    return """
    <html>
    <head><title>Forest Fire ML System</title></head>
    <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
        <div style="background: white; padding: 30px; border-radius: 10px;">
            <h1 style="color: #d32f2f;">🔥 Forest Fire Prediction System</h1>
            <p><strong>Status:</strong> ✅ Application Running Successfully</p>
            <p><strong>Platform:</strong> AWS Elastic Beanstalk</p>
            <p><strong>Framework:</strong> Flask 3.1.3</p>
            <hr>
            <p><a href="/health" style="color: #1976d2;">🔍 Health Check</a></p>
            <p><a href="/predict" style="color: #1976d2;">🔮 Make Prediction</a></p>
        </div>
    </body>
    </html>
    """

@application.route("/health")
def health():
    return {
        "status": "healthy",
        "message": "Forest Fire ML System is running",
        "platform": "AWS Elastic Beanstalk",
        "framework": "Flask 3.1.3"
    }

@application.route("/predict")
def predict():
    return """
    <html>
    <head><title>Forest Fire Prediction</title></head>
    <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
        <div style="background: white; padding: 30px; border-radius: 10px;">
            <h1 style="color: #d32f2f;">🔥 Forest Fire Risk Prediction</h1>
            <p>Prediction form will be available here.</p>
            <p><strong>Status:</strong> ✅ Route Working</p>
            <p><a href="/" style="color: #1976d2;">← Back to Home</a></p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    application.run(debug=True)
