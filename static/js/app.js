
console.log("CloudGuard Security dashboard loaded successfully.");

// Retrieve feature flag decisions from Flask.
async function loadSecurityFeatures() {
    try {
        const response = await fetch("/api/features");

        if (!response.ok) {
            throw new Error("Unable to retrieve security features");
        }

        const data = await response.json();
        const features = data.features;

        console.log("LaunchDarkly feature evaluation:", features);

        const sections = document.querySelectorAll("[data-feature-flag]");

        sections.forEach((section) => {
            const flagKey = section.dataset.featureFlag;
            const isEnabled = features[flagKey] === true;

            section.style.display = isEnabled ? "" : "none";

            console.log(`${flagKey}: ${isEnabled}`);
        });

    } catch (error) {
        console.error("Feature loading error:", error);
    }
}


// Send a question to the CloudGuard AI Security Analyst.
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
        statusElement.textContent = "Please enter a security question.";
        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Analyzing...";
    statusElement.textContent = "CloudGuard AI is analyzing your question...";
    responseContainer.hidden = true;
    responseElement.textContent = "";

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
            throw new Error(data.error || "AI analysis request failed.");
        }

        // Display the AI response safely as plain text.
        responseElement.textContent = data.response;
        responseElement.style.whiteSpace = "pre-wrap";

        responseContainer.hidden = false;
        statusElement.textContent = "Analysis completed successfully.";

    } catch (error) {
        console.error("AI Security Analyst error:", error);
        statusElement.textContent = error.message;
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Ask AI Security Analyst";
    }
}


// Run when the dashboard has loaded.
document.addEventListener("DOMContentLoaded", () => {

    console.log("Welcome to CloudGuard Security");

    loadSecurityFeatures();

    const aiButton = document.getElementById("ai-submit-button");

    if (aiButton) {
        aiButton.addEventListener("click", askAISecurityAnalyst);
    }
});
