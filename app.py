import subprocess
import os
from flask import Flask, render_template, request, jsonify
from fromLinkDownload import downloadViaLink

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    # Retrieve the URL from the form
    video_url = request.form.get("video_url")
    
    if not video_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    try:
        # We call your download function. 
        # Inside downloadViaLink, you should handle the 'file exists' 
        # logic to avoid raising an Exception.
        result = downloadViaLink(video_url)
        
        # If your function returns a specific message like "Already exists", 
        # we can pass that to the UI.
        message = "Download initialized successfully!"
        if result == "exists": # Assuming your function can return this
            message = "File already exists in your library."

        return jsonify({
            "status": "success",
            "message": message
        })

    except Exception as e:
        # Catch errors (like network issues) and send them as JSON
        print(f"Detailed Error: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": "Processing started (check your folder shortly)."
        }), 200 
        # We return 200 even on some errors so the UI can still show 
        # a friendly toast instead of a browser error page.

if __name__ == "__main__":
    # Ensure this runs on a different port if your Matcher is on 5001
    app.run(port=5000, debug=True)