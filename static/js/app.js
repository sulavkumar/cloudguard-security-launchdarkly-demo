
console.log("CloudGuard Security dashboard loaded successfully.");

// Retrieve feature flag decisions from Flask.
async function loadSecurityFeatures() {
    try {
        const response = await fetch("/api/features");

        if (!response.ok) {
            throw new Error("Unable to retrieve security features");
        }

        const data = await response.json();

        // Get the feature decisions returned by LaunchDarkly.
        const features = data.features;

        console.log("LaunchDarkly feature evaluation:", features);

        // Find dashboard sections controlled by feature flags.
        const sections = document.querySelectorAll("[data-feature-flag]");

        sections.forEach((section) => {

            // Read the LaunchDarkly flag associated with this section.
            const flagKey = section.dataset.featureFlag;

            // Check whether LaunchDarkly has enabled the feature.
            const isEnabled = features[flagKey] === true;

            // Show or hide the dashboard section.
            section.style.display = isEnabled ? "" : "none";

            console.log(`${flagKey}: ${isEnabled}`);
        });

    } catch (error) {
        console.error("Feature loading error:", error);
    }
}

// Run when the dashboard has loaded.
document.addEventListener("DOMContentLoaded", () => {
    console.log("Welcome to CloudGuard Security");
    loadSecurityFeatures();
});
