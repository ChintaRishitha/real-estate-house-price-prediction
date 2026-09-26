const $ = (id) => document.getElementById(id);

// =====================================================
// LOAD MODEL METRICS
// =====================================================

fetch("/metrics")
.then(response => {
if (!response.ok) {
throw new Error("Unable to load metrics");
}

    return response.json();
})

.then(metrics => {

    $("stat-records").textContent = metrics.records;

    $("stat-features").textContent = metrics.features;

    $("stat-r2").textContent = metrics.r2;

    $("stat-mae").textContent =
        "₹" + Number(metrics.mae).toLocaleString("en-IN");

    $("stat-rmse").textContent =
        "₹" + Number(metrics.rmse).toLocaleString("en-IN");


    // =============================================
    // LOAD LOCATIONS INTO DROPDOWN
    // =============================================

    const locationSelect = $("location");

    metrics.locations.forEach(location => {

        const option = document.createElement("option");

        option.value = location;

        option.textContent = location;

        locationSelect.appendChild(option);

    });

})

.catch(error => {

    console.error(
        "Could not load model metrics:",
        error
    );

});

// =====================================================
// FORMAT PRICE IN INDIAN RUPEES
// Example: ₹68,50,000
// =====================================================

function formatINR(number) {

return "₹" +
    Number(number).toLocaleString("en-IN");

}

// =====================================================
// PREDICTION FORM
// =====================================================

$("predict-form").addEventListener(
"submit",
async (event) => {

    event.preventDefault();


    // =============================================
    // GET USER INPUT
    // =============================================

    const payload = {

        area: $("area").value,

        bedrooms: $("bedrooms").value,

        bathrooms: $("bathrooms").value,

        floors: $("floors").value,

        parking: $("parking").value,

        age: $("age").value,

        location: $("location").value

    };


    // =============================================
    // CLIENT-SIDE VALIDATION
    // =============================================

    const area = Number(payload.area);

    const bedrooms = Number(payload.bedrooms);

    const bathrooms = Number(payload.bathrooms);

    const floors = Number(payload.floors);

    const parking = Number(payload.parking);

    const age = Number(payload.age);


    if (
        area < 200 ||
        area > 10000
    ) {

        showError(
            "Area must be between 200 and 10000 sq.ft."
        );

        return;

    }


    if (
        bedrooms < 1 ||
        bedrooms > 6
    ) {

        showError(
            "Bedrooms must be between 1 and 6."
        );

        return;

    }


    if (
        bathrooms < 1 ||
        bathrooms > 6
    ) {

        showError(
            "Bathrooms must be between 1 and 6."
        );

        return;

    }


    if (
        floors < 1 ||
        floors > 4
    ) {

        showError(
            "Floors must be between 1 and 4."
        );

        return;

    }


    if (
        parking < 0 ||
        parking > 4
    ) {

        showError(
            "Parking must be between 0 and 4."
        );

        return;

    }


    if (
        age < 0 ||
        age > 50
    ) {

        showError(
            "House age must be between 0 and 50 years."
        );

        return;

    }


    if (!payload.location) {

        showError(
            "Please select a location."
        );

        return;

    }


    // =============================================
    // RESET PREVIOUS RESULT
    // =============================================

    $("result-box").classList.add("hidden");

    $("error-box").classList.add("hidden");

    $("loader").classList.remove("hidden");

    $("predict-btn").disabled = true;


    // =============================================
    // SEND REQUEST TO FLASK
    // =============================================

    try {

        const response = await fetch(
            "/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(payload)
            }
        );


        const data =
            await response.json();


        // =========================================
        // HANDLE ERROR
        // =========================================

        if (!response.ok) {

            showError(
                data.error ||
                "Prediction failed."
            );

            return;

        }


        // =========================================
        // DISPLAY PREDICTED PRICE
        // =========================================

        $("result-price").textContent =
            formatINR(
                data.predicted_price
            );


        $("result-box")
            .classList
            .remove("hidden");


        // Scroll to result

        $("result-box").scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    }


    catch (error) {

        console.error(
            "Prediction error:",
            error
        );

        showError(
            "Server not reachable. Is Flask running?"
        );

    }


    finally {

        $("loader")
            .classList
            .add("hidden");

        $("predict-btn")
            .disabled = false;

    }

}

);

// =====================================================
// SHOW ERROR MESSAGE
// =====================================================

function showError(message) {

const errorBox =
    $("error-box");


errorBox.textContent =
    "⚠ " + message;


errorBox.classList
    .remove("hidden");


errorBox.scrollIntoView({
    behavior: "smooth",
    block: "center"
});

}