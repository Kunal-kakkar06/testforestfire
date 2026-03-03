from flask import Flask

application = Flask(__name__)

@application.route("/")
def hello():
    return """
    <h1>🔥 Test - Forest Fire App</h1>
    <p>✅ Flask is working!</p>
    <p>✅ Application deployed successfully!</p>
    <p><a href="/health">Health Check</a></p>
    <p><a href="/test">Test Route</a></p>
    """

@application.route("/health")
def health():
    return {
        "status": "healthy",
        "message": "Simple Flask app is working",
        "routes": ["/" , "/health", "/test"]
    }

@application.route("/test")
def test():
    return "<h2>✅ Test route is working!</h2><p><a href='/'>Back to Home</a></p>"

if __name__ == "__main__":
    application.run(debug=True)
