
import numpy as np
import tensorflow as tf

from PIL import Image
from huggingface_hub import hf_hub_download


CLASS_NAMES = [
    "Corn - Common Rust",
    "Potato - Early Blight",
    "Tomato - Bacterial Spot"
]

MODEL = None


def load_disease_model():

    global MODEL

    if MODEL is None:

        model_path = hf_hub_download(
            repo_id="Noor-Khan/plant-disease-prediction",
            filename="plant_disease_cnn.keras"
        )

        MODEL = tf.keras.models.load_model(model_path)

    return MODEL


def predict_disease(image_path):

    model = load_disease_model()

    image = Image.open(image_path).convert("RGB")
    image = image.resize((256, 256))

    image_array = np.array(image, dtype=np.float32)
    image_array = image_array / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array, verbose=0)[0]

    predicted_index = int(np.argmax(predictions))

    return {
        "disease": CLASS_NAMES[predicted_index],
        "confidence": round(
            float(predictions[predicted_index]) * 100, 2
        )
    }
