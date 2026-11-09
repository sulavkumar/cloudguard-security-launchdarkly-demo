# CloudGuard Security – CNAPP & AI Security Analyst Demo

CloudGuard Security is a demonstration Cloud-Native Application Protection Platform (CNAPP) built with Python Flask and LaunchDarkly. It showcases feature management, controlled feature releases, real-time feature flag updates, cloud security visibility, and an AI-powered Security Analyst using LaunchDarkly AgentControl and OpenAI.

The project demonstrates how organizations can introduce AI-powered security capabilities while retaining centralized control over feature availability, AI configuration, and evaluation.

## Project Overview

CloudGuard provides a simulated enterprise cloud security dashboard with the following capabilities:

- Cloud asset inventory
- Vulnerability management
- Cloud security posture visibility
- Threat detection
- Automated remediation feature module
- AI-powered security analysis
- Real-time feature flag updates without manual browser refresh

The application uses LaunchDarkly feature flags to control the availability of individual security modules.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Feature management | LaunchDarkly Server-side SDK |
| Real-time communication | Server-Sent Events (SSE) |
| Browser event handling | JavaScript EventSource API |
| AI configuration | LaunchDarkly AgentControl |
| AI model | OpenAI GPT-4o |
| AI framework | OpenAI Agents SDK |
| AI integration | LaunchDarkly AI SDK for Python |
| Environment configuration | python-dotenv |

## Architecture

### Application architecture

```text
                  CloudGuard Dashboard
                     HTML / CSS / JS
                            |
                            v
                     Python Flask App
                            |
              +-------------+-------------+
              |                           |
              v                           v
       LaunchDarkly SDK              AI Security API
              |                           |
              v                           v
        Feature Flags              LaunchDarkly AgentControl
              |                           |
              v                           v
       Module Visibility              Agent Configuration
                                          |
                             +------------+------------+
                             |            |            |
                             v            v            v
                           GPT-4o     Custom Skill    Judges
                             |
                             v
                         OpenAI API
                             |
                             v
                     AI Security Analysis
                             |
                             v
                     CloudGuard Dashboard
```

### Real-time feature flag architecture

CloudGuard uses LaunchDarkly flag value change listeners and Flask Server-Sent Events (SSE) to deliver feature updates to connected browsers.

```text
       LaunchDarkly Console
                |
                | Feature flag value changes
                v
      LaunchDarkly Python SDK
                |
                | Flag value change listener
                v
          Flask Backend
                |
                | Publish flag update
                v
       SSE Endpoint
       /api/feature-events
                |
                | Persistent HTTP connection
                v
       Browser EventSource API
                |
                | JavaScript processes update
                v
       CloudGuard Dashboard
                |
                v
       UI updates automatically
       Without manual page refresh
```

### How real-time updates work

1. An administrator enables or disables a feature flag in LaunchDarkly.
2. The LaunchDarkly Python Server-side SDK detects a change in the evaluated flag value for the configured customer context.
3. A registered flag value change listener receives the update.
4. Flask publishes the updated flag value to connected browser clients.
5. The browser receives the update through the JavaScript EventSource API.
6. JavaScript identifies the corresponding dashboard section and updates its visibility.

The browser maintains a persistent SSE connection, allowing the dashboard to receive updates without requiring a manual page refresh.

The SSE endpoint also sends the initial feature flag evaluations when a browser connects.

## LaunchDarkly Feature Flags

The application uses the following Boolean feature flags:

| Feature flag | Purpose |
|---|---|
| `new_security_dashboard` | Controls the updated security dashboard |
| `advanced_vulnerability_scanning` | Controls vulnerability management visibility |
| `threat_detection_enabled` | Controls threat detection visibility |
| `auto_remediation_enabled` | Controls the remediation module |
| `ai_security_assistant` | Controls the AI Security Analyst module |

Feature flag evaluations are performed server-side through the LaunchDarkly Python SDK.

### Customer Context

The application evaluates feature flags using the following customer context:

| Attribute | Value |
|---|---|
| Context key | `security_admin_001` |
| Name | Security Administrator |
| User tier | Standard |
| Geography | India |
| Environment | Production |

LaunchDarkly targeting rules determine which features are enabled for this context.

## Real-Time Feature Flag Updates

CloudGuard supports real-time feature flag updates using:

- LaunchDarkly Python SDK flag value change listeners
- Flask SSE endpoint
- JavaScript EventSource API

### SSE Endpoint

```text
GET /api/feature-events
```

The endpoint maintains a persistent connection with the browser and sends:

- Initial feature flag evaluations when the connection is established.
- Individual feature flag updates when a monitored flag changes.
- Periodic heartbeat messages to keep the connection alive.

### Frontend Integration

The JavaScript frontend subscribes to the SSE endpoint:

```javascript
const eventSource = new EventSource("/api/feature-events");
```

When a feature flag update is received, the frontend identifies the corresponding HTML section using its `data-feature-flag` attribute and updates its visibility.

Example:

```html
<section data-feature-flag="ai_security_assistant">
    <!-- AI Security Analyst content -->
</section>
```

This separates feature evaluation and event delivery from frontend presentation.

## LaunchDarkly AgentControl Integration

CloudGuard integrates with LaunchDarkly AgentControl to manage AI behavior independently of the application code.

### Agent Configuration

- Name: CloudGuard AI Security Analyst
- Config key: `cloud-guard-ai-security-analyst`
- Mode: Agent
- Variation: CloudGuard Security Analyst v1
- Model: OpenAI GPT-4o
- Environment: Test

### Custom AI Skill

A custom skill named `Cloud Security Analysis` is attached to the Agent.

It provides structured guidance for:

1. Vulnerability management
2. Cloud security posture analysis
3. Threat detection
4. Identity and access management risks
5. Remediation recommendations

The Agent is instructed to distinguish confirmed findings from assumptions and avoid inventing scan results or claiming that remediation has been completed without evidence.

### AI Judges

Two LaunchDarkly Judges are configured:

- **Accuracy:** Evaluates factual correctness.
- **Relevance:** Evaluates whether responses address the user's question.

Both Judges use the OpenAI provider and are configured with 10% sampling.

Judge configuration is present in LaunchDarkly; evaluation scores should be reviewed in the Monitoring interface.

## AI Security Analyst – Demonstration

Users can interact with the AI Security Analyst directly from the CloudGuard dashboard.

Example question:

> An AWS EC2 server has SSH port 22 exposed to the public internet. What are the security risks and how should I remediate them?

The Agent provides:

- Security risk identification
- Severity assessment
- Potential business impact
- Recommended remediation steps
- Security best practices

The dashboard sends questions to the Flask backend, which invokes the LaunchDarkly AgentControl configuration and returns the generated response.

## Application Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Loads the CloudGuard dashboard |
| `/api/features` | GET | Returns LaunchDarkly feature flag evaluations |
| `/api/feature-events` | GET | Streams real-time feature flag updates using SSE |
| `/api/health` | GET | Returns application health information |
| `/api/scan/success` | GET | Simulates a successful vulnerability scan event |
| `/api/scan/failure` | GET | Simulates a failed vulnerability scan event |
| `/api/ai/ask` | POST | Sends a question to the AI Security Analyst |

Example AI request:

```json
{
  "question": "What are the security risks of exposing SSH to the internet?"
}
```

## Project Structure

```text
cloudguard-security/
│
├── app.py
├── test_openai.py
├── test_agentcontrol.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── app.js
```

## Installation and Setup

### Prerequisites

- Python 3.12 or later
- A LaunchDarkly account
- An OpenAI API account with API access and billing enabled
- Git

### 1. Clone the repository

```bash
git clone https://github.com/sulavkumar/cloudguard-security-launchdarkly-demo.git

cd cloudguard-security-launchdarkly-demo
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
LAUNCHDARKLY_SDK_KEY=your_launchdarkly_sdk_key
OPENAI_API_KEY=your_openai_api_key
```

Never commit `.env` or expose API keys in frontend code.

### 5. Configure LaunchDarkly

Create the required feature flags in your LaunchDarkly project.

Configure the AI Agent using the following config key:

```text
cloud-guard-ai-security-analyst
```

Ensure the AgentControl configuration is enabled and the intended variation is served in the Test environment.

### 6. Run the application

```powershell
python app.py
```

Open the dashboard:

```text
http://127.0.0.1:5000
```

## Testing the Integration

### Verify the OpenAI connection

```powershell
python test_openai.py
```

### Test the LaunchDarkly AgentControl integration

```powershell
python test_agentcontrol.py
```

### Verify application health

```text
http://127.0.0.1:5000/api/health
```

### Verify feature flag evaluations

```text
http://127.0.0.1:5000/api/features
```

### Test real-time feature updates

1. Start the CloudGuard application.
2. Open the dashboard in a browser.
3. Open browser Developer Tools and select Console.
4. Confirm that the SSE connection is established.
5. Open LaunchDarkly in another browser tab.
6. Toggle one of the five feature flags.
7. Observe the corresponding dashboard section.

Expected behavior: The corresponding dashboard section updates automatically without manually refreshing the browser.

## Key Demonstration Scenarios

### 1. Feature Management

Enable or disable individual CloudGuard security modules using LaunchDarkly feature flags.

### 2. Controlled Rollouts

Demonstrate progressive rollout configurations for security capabilities using LaunchDarkly.

### 3. Customer Targeting

Use LaunchDarkly context attributes such as customer tier and geography to demonstrate targeted feature availability.

### 4. Real-Time Feature Updates

Demonstrate how LaunchDarkly flag changes are propagated to the CloudGuard dashboard using Python SDK listeners and SSE, without manual browser refresh.

### 5. AI Configuration Management

Change the AI model, Agent instructions, and custom skills through LaunchDarkly AgentControl.

### 6. AI Security Analysis

Submit cloud security questions through the dashboard and receive AI-generated security recommendations.

### 7. AI Evaluation

Use Accuracy and Relevance Judges to evaluate AI-generated responses and review evaluation data in LaunchDarkly Monitoring.

## Important Notes

- This is a demonstration application, not a production CNAPP platform.
- Dashboard asset counts, vulnerability findings, posture scores, and threat alerts are sample data.
- Vulnerability scan endpoints simulate success and failure events; they do not execute real infrastructure scans.
- The remediation module is a demonstration capability and does not modify cloud infrastructure.
- The AI Security Analyst provides advisory recommendations and does not perform infrastructure remediation.
- OpenAI API usage is billed separately from ChatGPT subscriptions.
- Protect all API keys and LaunchDarkly SDK credentials.
- Real-time UI updates depend on successful LaunchDarkly listener registration, SSE connectivity, and frontend event handling.

## Learning Objectives

This project demonstrates practical implementation of:

- Feature management and progressive delivery
- Context-based targeting
- Real-time feature flag updates
- Server-Sent Events
- Flask API integration
- AI configuration management
- Agent-based AI integration
- Custom AI skills
- AI response evaluation
- Secure management of application credentials

## Repository

GitHub: https://github.com/sulavkumar/cloudguard-security-launchdarkly-demo

**CloudGuard Security – Demonstrating Feature Management and AI-powered Cloud Security.**