
import os
import logging
import asyncio

import ldclient
from ldclient import Context
from ldclient.config import Config

from launchdarkly_ai_server import config, init_client, shutdown
from launchdarkly_ai_openai_agents import create_openai_agents_handler

from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

# Load configuration from the .env file
load_dotenv()

# Create Flask application
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# Initialize LaunchDarkly
sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY")

ld_client = None

if sdk_key:
    ldclient.set_config(Config(sdk_key))
    ld_client = ldclient.get()

    if ld_client.is_initialized():
        print("LaunchDarkly connected successfully!")
    else:
        print("LaunchDarkly SDK is not initialized yet.")
else:
    print("WARNING: LaunchDarkly SDK key is missing.")


# Create a demo customer context
def create_customer_context():

    return (
        Context.builder("security_admin_001")
        .kind("user")
        .name("Security Administrator")
        .set("user_tier", "Standard")
        .set("geography", "India")
        .set("environment", "Production")
        .build()
    )

# Send vulnerability scan events to LaunchDarkly
def record_scan_event(event_key):

    context = create_customer_context()

    if ld_client and ld_client.is_initialized():

        ld_client.track(event_key, context)

        print(f"LaunchDarkly event sent: {event_key}")

    else:
        print("LaunchDarkly is not initialized. Event not sent.")


# Evaluate CloudGuard feature flags
def evaluate_security_features():

    context = create_customer_context()

    flag_keys = [
        "new_security_dashboard",
        "advanced_vulnerability_scanning",
        "threat_detection_enabled",
        "auto_remediation_enabled",
        "ai_security_assistant"
    ]

    features = {}

    for flag_key in flag_keys:

        if ld_client and ld_client.is_initialized():

            features[flag_key] = ld_client.variation(
                flag_key,
                context,
                False
            )

        else:
            features[flag_key] = False

    return features



# Simulate vulnerability scan results
@app.route("/api/scan/<result>")
def simulate_scan(result):

    if result == "success":

        record_scan_event("vulnerability_scan_success")

        return jsonify({
            "scan_status": "success",
            "message": "Vulnerability scan completed successfully."
        })

    elif result == "failure":

        record_scan_event("vulnerability_scan_failure")

        return jsonify({
            "scan_status": "failure",
            "message": "Vulnerability scan failed."
        })

    else:

        return jsonify({
            "error": "Invalid scan result. Use success or failure."
        }), 400


# CloudGuard AI Security Analyst endpoint
@app.route("/api/ai/ask", methods=["POST"])
def ask_ai_security_analyst():

    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "error": "Please provide a security question."
        }), 400

    if not ld_client or not ld_client.is_initialized():
        return jsonify({
            "error": "LaunchDarkly is not initialized."
        }), 503

    async def invoke_agent():

        await init_client(client=ld_client)

        context = {
            "kind": "user",
            "key": "security_admin_001",
            "name": "Security Administrator",
            "user_tier": "Standard",
            "geography": "India",
            "environment": "Production"
        }

        agent = config(
            key="cloud-guard-ai-security-analyst",
            handler=create_openai_agents_handler()
        )

        return await agent.invoke(question, context)

    try:
        result = asyncio.run(invoke_agent())

        return jsonify({
            "response": result.response
        })

    except Exception:
        logging.exception("CloudGuard AI Agent invocation failed.")

        return jsonify({
            "error": "The AI Security Analyst could not process your request. Please try again."
        }), 500

# Display the CloudGuard dashboard
@app.route("/")
def home():
    return render_template("index.html")


# API endpoint for LaunchDarkly feature evaluations
@app.route("/api/features")
def get_features():

    features = evaluate_security_features()

    return jsonify({
        "customer": "security_admin_001",
        "customer_tier": "Standard",
        "launchdarkly_initialized": (
            ld_client.is_initialized() if ld_client else False
        ),
        "features": features
    })


# Application health endpoint
@app.route("/api/health")
def health():

    return jsonify({
        "application": "CloudGuard Security",
        "status": "running",
        "launchdarkly_initialized": (
            ld_client.is_initialized() if ld_client else False
        )
    })


if __name__ == "__main__":

    print("Starting CloudGuard Security...")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
