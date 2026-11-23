
def assess_crop_health(crop, temperature, humidity, rainfall):

    crop = crop.lower()

    results = []
    risk_score = 0

    # Temperature assessment
    if temperature >= 40:
        results.append("Very high temperature: possible heat stress.")
        risk_score += 3
    elif temperature >= 35:
        results.append("High temperature: monitor for heat stress.")
        risk_score += 2
    elif temperature <= 10:
        results.append("Low temperature: monitor for cold stress.")
        risk_score += 2
    else:
        results.append("No extreme temperature detected by this screening rule.")

    # Humidity assessment
    if humidity >= 90:
        results.append(
            "Very high humidity: conditions may favour fungal diseases."
        )
        risk_score += 3
    elif humidity >= 80:
        results.append(
            "High humidity: monitor leaves for fungal symptoms."
        )
        risk_score += 2
    elif humidity <= 30:
        results.append(
            "Low humidity: monitor plants for moisture stress."
        )
        risk_score += 1
    else:
        results.append("Humidity is not extreme under this screening rule.")

    # Rainfall assessment
    if rainfall >= 100:
        results.append(
            "Heavy rainfall: check for waterlogging and drainage problems."
        )
        risk_score += 3
    elif rainfall >= 50:
        results.append(
            "Substantial rainfall: inspect soil drainage."
        )
        risk_score += 2
    elif rainfall == 0:
        results.append(
            "No rainfall reported: check soil moisture."
        )
        risk_score += 1

    # Screening category
    if risk_score >= 6:
        risk_level = "High"
    elif risk_score >= 3:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    return {
        "crop": crop.title(),
        "risk_level": risk_level,
        "risk_score": risk_score,
        "observations": results,
        "recommendation": get_recommendation(risk_level)
    }


def get_recommendation(risk_level):

    if risk_level == "High":
        return (
            "Inspect the crop promptly, check soil drainage and "
            "look for visible stress symptoms."
        )

    elif risk_level == "Moderate":
        return (
            "Monitor the crop regularly and check soil moisture "
            "and leaf condition."
        )

    return (
        "Continue routine crop monitoring and follow local "
        "agricultural advisories."
    )
