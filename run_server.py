from core.network.server import app

if name == "main":
    print("Starting Jarvis Network Server on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)