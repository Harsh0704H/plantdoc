
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from crop_guardian import assess_crop_health
from weather import get_weather
from disease_model import predict_disease
from combined_engine import generate_plant_report
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

os.makedirs("uploads", exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload_image():

    if "image" not in request.files:
        return jsonify({"error": "No image selected"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Please select an image"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid image format"}), 400

    filename = secure_filename(file.filename)

    try:
        from PIL import Image

        file.stream.seek(0)
        image = Image.open(file.stream)
        image.verify()
        file.stream.seek(0)

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

    except Exception:
        return jsonify({"error": "The uploaded file is not a valid image"}), 400

    try:
        prediction = predict_disease(filepath)

        return jsonify({
            "message": "Analysis completed",
            "filename": filename,
            "disease": prediction["disease"],
            "confidence": prediction["confidence"]
        })

    except Exception:
        app.logger.exception("Disease prediction failed")

        return jsonify({
            "error": "Image saved, but AI analysis failed. Check the server."
        }), 500
    


@app.route("/api/assess", methods=["POST"])
def assess():

    data = request.get_json()

    try:
        crop = data["crop"]
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        rainfall = float(data["rainfall"])

        if not 0 <= humidity <= 100:
            return jsonify({"error": "Humidity must be between 0 and 100"}), 400

        if temperature < -50 or temperature > 60:
            return jsonify({"error": "Invalid temperature"}), 400

        if rainfall < 0:
            return jsonify({"error": "Rainfall cannot be negative"}), 400

        result = assess_crop_health(
            crop, temperature, humidity, rainfall
        )

        return jsonify(result)

    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Please enter valid crop and weather values"}), 400


@app.route("/api/weather", methods=["POST"])
def weather():

    data = request.get_json(silent=True) or {}
    city = data.get("city", "").strip()

    if not city:
        return jsonify({"error": "Please enter a city name"}), 400

    result = get_weather(city)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result)

@app.route("/api/combined-report", methods=["POST"])
def combined_report():

    data = request.get_json(silent=True) or {}

    try:
        filename = data["filename"]
        crop = data["crop"]
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        rainfall = float(data["rainfall"])

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        if not os.path.isfile(filepath):
            return jsonify({"error": "Please upload a plant image first"}), 404

        if not 0 <= humidity <= 100:
            return jsonify({"error": "Humidity must be between 0 and 100"}), 400

        if temperature < -50 or temperature > 60 or rainfall < 0:
            return jsonify({"error": "Invalid weather values"}), 400

        report = generate_plant_report(
            filepath,
            crop,
            temperature,
            humidity,
            rainfall
        )

        return jsonify(report)

    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Please provide valid report details"}), 400

    except Exception:
        app.logger.exception("Combined report failed")
        return jsonify({"error": "Could not generate the combined report"}), 500
if __name__ == "__main__":
    app.run(debug=True)
