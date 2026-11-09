console.log("CloudGuard Security dashboard loaded successfully.");

// --------------------------------------------------
// Apply a feature flag value to the dashboard
// --------------------------------------------------

function applyFeatureFlag(flagKey, isEnabled) {
    const sections = document.querySelectorAll("[data-feature-flag]");

    sections.forEach((section) => {
        if (section.dataset.featureFlag === flagKey) {
            section.style.display = isEnabled ? "" : "none";

            console.log(
                `Dashboard updated: ${flagKey} = ${isEnabled}`
            );
        }
    });
}


// --------------------------------------------------
// Apply all initial feature flag values
// --------------------------------------------------

function applyAllFeatures(features) {
    Object.entries(features).forEach(([flagKey, isEnabled]) => {
        applyFeatureFlag(flagKey, isEnabled === true);
    });

    console.log("Initial LaunchDarkly features applied:", features);
}


// --------------------------------------------------
// Establish real-time updates using Server-Sent Events
// --------------------------------------------------

function connectToFeatureUpdates() {
    console.log("Connecting to CloudGuard real-time feature updates...");

    const eventSource = new EventSource("/api/feature-events");

    eventSource.onopen = () => {
        console.log("Connected to CloudGuard feature update stream.");
    };

    eventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);

            // Initial feature values sent when the connection opens.
            if (data.type === "initial") {
                applyAllFeatures(data.features);
                return;
            }

            // Individual LaunchDarkly feature flag update.
            if (data.type === "flag_update") {
                console.log(
                    "Received LaunchDarkly update:",
                    data.flag,
                    data.value
                );

                applyFeatureFlag(data.flag, data.value === true);
            }
        } catch (error) {
            console.error("Unable to process feature update:", error);
        }
    };

    eventSource.onerror = (error) => {
        console.error(
            "Feature update connection interrupted. Reconnecting...",
            error
        );

        // EventSource automatically attempts to reconnect.
    };

    return eventSource;
}


// --------------------------------------------------
// Send a question to CloudGuard AI Security Analyst
// --------------------------------------------------

async function askAISecurityAnalyst() {
    const questionInput = document.getElementById("ai-question");
    const submitButton = document.getElementById("ai-submit-button");
    const statusElement = document.getElementById("ai-status");
    const responseContainer = document.getElementById("ai-response-container");
    const responseElement = document.getElementById("ai-response");

    if (!questionInput || !submitButton) {
        return;
    }

    const question = questionInput.value.trim();

    if (!question) {
        if (statusElement) {
            statusElement.textContent = "Please enter a security question.";
        }
        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Analyzing...";

    if (statusElement) {
        statusElement.textContent =
            "CloudGuard AI is analyzing your question...";
    }

    if (responseContainer) {
        responseContainer.hidden = true;
    }

    if (responseElement) {
        responseElement.textContent = "";
    }

    try {
        const response = await fetch("/api/ai/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "AI analysis request failed."
            );
        }

        // Display the AI response safely as plain text.
        if (responseElement) {
            responseElement.textContent = data.response;
            responseElement.style.whiteSpace = "pre-wrap";
        }

        if (responseContainer) {
            responseContainer.hidden = false;
        }

        if (statusElement) {
            statusElement.textContent =
                "Analysis completed successfully.";
        }

    } catch (error) {
        console.error("AI Security Analyst error:", error);

        if (statusElement) {
            statusElement.textContent = error.message;
        }

    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Ask AI Security Analyst";
    }
}


// --------------------------------------------------
// Initialize CloudGuard dashboard
// --------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
    console.log("Welcome to CloudGuard Security.");

    // Open a persistent connection for real-time flag updates.
    connectToFeatureUpdates();

    // Connect the AI Security Analyst button.
    const aiButton = document.getElementById("ai-submit-button");

    if (aiButton) {
        aiButton.addEventListener("click", askAISecurityAnalyst);
    }
});