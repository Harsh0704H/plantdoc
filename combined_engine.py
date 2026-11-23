
from disease_model import predict_disease
from crop_guardian import assess_crop_health


def generate_plant_report(
    image_path,
    crop,
    temperature,
    humidity,
    rainfall
):
    # 1. Analyze the uploaded plant image
    disease_result = predict_disease(image_path)

    # 2. Assess environmental conditions
    crop_result = assess_crop_health(
        crop,
        temperature,
        humidity,
        rainfall
    )

    # 3. Combine both results
    report = {
        "plant_analysis": {
            "predicted_disease": disease_result["disease"],
            "confidence": disease_result["confidence"],
            "notice": "Experimental AI classification, not a confirmed diagnosis."
        },

        "environment_analysis": {
            "crop": crop_result["crop"],
            "risk_level": crop_result["risk_level"],
            "risk_score": crop_result["risk_score"],
            "observations": crop_result["observations"],
            "recommendation": crop_result["recommendation"]
        }
    }

    return report
