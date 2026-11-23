
const uploadForm = document.getElementById("uploadForm");

uploadForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const image = document.getElementById("plantImage").files[0];
    const result = document.getElementById("uploadResult");

    if (!image) {
        result.textContent = "Please select an image.";
        return;
    }

    const formData = new FormData();
    formData.append("image", image);

    result.textContent = "Uploading image...";

    try {
        const response = await fetch("/api/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
    result.textContent = data.error;
    return;
}
window.lastUploadedFilename = data.filename;
result.innerHTML = `
    <h3>AI Analysis Result</h3>
    <p><b>Predicted disease:</b> ${data.disease}</p>
    <p><b>Model confidence:</b> ${data.confidence}%</p>
    <p><small>Experimental AI prediction. This is not a confirmed plant diagnosis.</small></p>
`;

    } catch (error) {
        result.textContent = "Something went wrong.";
    }

});

document.getElementById("assessButton").addEventListener("click", async function () {

    const crop = document.getElementById("crop").value;
    const temperature = document.getElementById("temperature").value;
    const humidity = document.getElementById("humidity").value;
    const rainfall = document.getElementById("rainfall").value;

    const resultBox = document.getElementById("riskResult");

    if (temperature === "" || humidity === "" || rainfall === "") {
        resultBox.textContent = "Please fill in all weather values.";
        return;
    }

    resultBox.textContent = "Assessing crop conditions...";

    try {
        const response = await fetch("/api/assess", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                crop: crop,
                temperature: temperature,
                humidity: humidity,
                rainfall: rainfall
            })
        });

        const data = await response.json();

        if (!response.ok) {
            resultBox.textContent = data.error;
            return;
        }

        resultBox.innerHTML = `
            <h3>Crop Health Assessment</h3>
            <p><b>Crop:</b> ${data.crop}</p>
            <p><b>Environmental risk:</b> ${data.risk_level}</p>
            <h4>Observations</h4>
            <ul>
                ${data.observations.map(item => `<li>${item}</li>`).join("")}
            </ul>
            <p><b>Recommendation:</b> ${data.recommendation}</p>
            <small>Rule-based screening, not a validated disease or crop-failure prediction.</small>
        `;

    } catch (error) {
        resultBox.textContent = "Could not assess crop conditions.";
    }
});

document.getElementById("weatherButton").addEventListener("click", async function () {

    const city = document.getElementById("city").value.trim();
    const result = document.getElementById("weatherResult");

    if (!city) {
        result.textContent = "Please enter your city.";
        return;
    }

    result.textContent = "Fetching live weather...";

    try {
        const response = await fetch("/api/weather", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ city: city })
        });

        const data = await response.json();

        if (!response.ok) {
            result.textContent = data.error;
            return;
        }

        document.getElementById("temperature").value = data.temperature;
        document.getElementById("humidity").value = data.humidity;
        document.getElementById("rainfall").value = data.rainfall;

        result.textContent =
            `Weather loaded for ${data.city}, ${data.country}. ` +
            `Temperature: ${data.temperature}°C, ` +
            `Humidity: ${data.humidity}%, ` +
            `Current precipitation: ${data.rainfall} mm.`;

    } catch (error) {
        result.textContent = "Could not connect to weather service.";
    }
});

const combinedButton = document.getElementById("combinedReportButton");
const combinedResult = document.getElementById("combinedReportResult");

if (combinedButton && combinedResult) {
    combinedButton.addEventListener("click", async () => {
        combinedResult.textContent = "Generating PlantDoc report...";

        const filename = window.lastUploadedFilename;

        if (!filename) {
            combinedResult.textContent = "Please upload a plant image first.";
            return;
        }

        const crop = document.getElementById("crop").value;
        const temperature = document.getElementById("temperature").value;
        const humidity = document.getElementById("humidity").value;
        const rainfall = document.getElementById("rainfall").value;

        try {
            const response = await fetch("/api/combined-report", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    filename,
                    crop,
                    temperature,
                    humidity,
                    rainfall
                })
            });

            const data = await response.json();

            if (!response.ok) {
                combinedResult.textContent = data.error || "Report failed.";
                return;
            }

            const plant = data.plant_analysis;
            const environment = data.environment_analysis;

            combinedResult.innerHTML = `
                <h3>Plant Disease Analysis</h3>
                <p><b>Predicted disease:</b> ${plant.predicted_disease}</p>
                <p><b>Confidence:</b> ${plant.confidence}%</p>
                <p>${plant.notice}</p>

                <hr>

                <h3>Environmental Risk Assessment</h3>
                <p><b>Crop:</b> ${environment.crop}</p>
                <p><b>Risk level:</b> ${environment.risk_level}</p>
                <p><b>Risk score:</b> ${environment.risk_score}</p>
                <p><b>Recommendation:</b> ${environment.recommendation}</p>

                <h4>Observations</h4>
                <ul>
                    ${environment.observations.map(item => `<li>${item}</li>`).join("")}
                </ul>
            `;
        } catch (error) {
            combinedResult.textContent = "Could not connect to PlantDoc server.";
        }
    });
}
