
import os
import json
import logging
import asyncio
import queue
import threading

import ldclient
from ldclient import Context
from ldclient.config import Config

from launchdarkly_ai_server import config, init_client, shutdown
from launchdarkly_ai_openai_agents import create_openai_agents_handler

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    Response,
    stream_with_context
)

from dotenv import load_dotenv

# --------------------------------------------------
# Application configuration
# --------------------------------------------------

load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# --------------------------------------------------
# LaunchDarkly initialization
# --------------------------------------------------

sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY")

ld_client = None

FLAG_KEYS = [
    "new_security_dashboard",
    "advanced_vulnerability_scanning",
    "threat_detection_enabled",
    "auto_remediation_enabled",
    "ai_security_assistant"
]

# SSE client queues and synchronization
sse_clients = []
sse_lock = threading.Lock()

if sdk_key:
    ldclient.set_config(Config(sdk_key))
    ld_client = ldclient.get()

    if ld_client.is_initialized():
        print("LaunchDarkly connected successfully!")
    else:
        print("LaunchDarkly SDK is not initialized yet.")
else:
    print("WARNING: LaunchDarkly SDK key is missing.")


# --------------------------------------------------
# Customer context
# --------------------------------------------------

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


# --------------------------------------------------
# Evaluate CloudGuard feature flags
# --------------------------------------------------

def evaluate_security_features():

    context = create_customer_context()

    features = {}

    for flag_key in FLAG_KEYS:

        if ld_client and ld_client.is_initialized():

            features[flag_key] = ld_client.variation(
                flag_key,
                context,
                False
            )

        else:
            features[flag_key] = False

    return features


# --------------------------------------------------
# Send updates to connected browser clients
# --------------------------------------------------

def publish_flag_update(flag_key, flag_value):

    message = json.dumps({
        "type": "flag_update",
        "flag": flag_key,
        "value": flag_value
    })

    with sse_lock:

        disconnected_clients = []

        for client_queue in sse_clients:

            try:
                client_queue.put_nowait(message)

            except queue.Full:
                disconnected_clients.append(client_queue)

        for client_queue in disconnected_clients:

            sse_clients.remove(client_queue)


# --------------------------------------------------
# LaunchDarkly flag change listeners
# --------------------------------------------------

def register_flag_listeners():

    if not ld_client or not ld_client.is_initialized():

        logging.warning(
            "LaunchDarkly is not initialized. Listeners not registered."
        )

        return

    context = create_customer_context()

    def create_callback(flag_key):

        def on_flag_value_change(event):

            # Re-evaluate the flag for our customer context.
            new_value = ld_client.variation(
                flag_key,
                context,
                False
            )

            logging.info(
                "LaunchDarkly flag changed: %s = %s",
                flag_key,
                new_value
            )

            # Send the update to connected browsers.
            publish_flag_update(flag_key, new_value)

        return on_flag_value_change

    tracker = ld_client.flag_tracker

    for flag_key in FLAG_KEYS:

        tracker.add_flag_value_change_listener(
            flag_key,
            context,
            create_callback(flag_key)
        )

    logging.info(
        "Registered LaunchDarkly listeners for all five flags."
    )


# --------------------------------------------------
# Server-Sent Events endpoint
# --------------------------------------------------

@app.route("/api/feature-events")
def feature_events():

    client_queue = queue.Queue(maxsize=20)

    with sse_lock:
        sse_clients.append(client_queue)

    def event_stream():

        try:

            # Send current feature flag values immediately.
            initial_features = evaluate_security_features()

            yield "data: " + json.dumps({
                "type": "initial",
                "features": initial_features
            }) + "\n\n"

            while True:

                try:

                    message = client_queue.get(timeout=20)

                    yield "data: " + message + "\n\n"

                except queue.Empty:

                    # Keep the SSE connection alive.
                    yield ": heartbeat\n\n"

        finally:

            with sse_lock:

                if client_queue in sse_clients:
                    sse_clients.remove(client_queue)

    return Response(
        stream_with_context(event_stream()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive"
        }
    )


# --------------------------------------------------
# Vulnerability scan events
# --------------------------------------------------

def record_scan_event(event_key):

    context = create_customer_context()

    if ld_client and ld_client.is_initialized():

        ld_client.track(event_key, context)

        print(f"LaunchDarkly event sent: {event_key}")

    else:

        print("LaunchDarkly is not initialized. Event not sent.")


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


# --------------------------------------------------
# CloudGuard AI Security Analyst
# --------------------------------------------------

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

        logging.exception(
            "CloudGuard AI Agent invocation failed."
        )

        return jsonify({
            "error": (
                "The AI Security Analyst could not process "
                "your request. Please try again."
            )
        }), 500


# --------------------------------------------------
# CloudGuard dashboard
# --------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# --------------------------------------------------
# Feature flag API
# --------------------------------------------------

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


# --------------------------------------------------
# Application health
# --------------------------------------------------

@app.route("/api/health")
def health():

    return jsonify({
        "application": "CloudGuard Security",
        "status": "running",
        "launchdarkly_initialized": (
            ld_client.is_initialized() if ld_client else False
        )
    })


# --------------------------------------------------
# Start application
# --------------------------------------------------

if __name__ == "__main__":

    print("Starting CloudGuard Security...")

    register_flag_listeners()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True
    )
