# CloudGuard Security – CNAPP & AI Security Analyst Demo

CloudGuard Security is a demonstration Cloud-Native Application Protection Platform (CNAPP) built with Python Flask and LaunchDarkly. It showcases feature management, controlled feature releases, cloud security visibility, and an AI-powered Security Analyst using LaunchDarkly AgentControl and OpenAI.

The project demonstrates how organizations can introduce AI-powered security capabilities while retaining centralized control over AI configuration, feature availability, and evaluation.

## Project Overview

CloudGuard provides a simulated enterprise cloud security dashboard with the following capabilities:

- Cloud asset inventory
- Vulnerability management
- Cloud security posture visibility
- Threat detection
- Automated remediation feature module
- AI-powered security analysis

The application uses LaunchDarkly feature flags to control the availability of individual security modules.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Feature management | LaunchDarkly Server-side SDK |
| AI configuration | LaunchDarkly AgentControl |
| AI model | OpenAI GPT-4o |
| AI framework | OpenAI Agents SDK |
| AI integration | LaunchDarkly AI SDK for Python |
| Environment configuration | python-dotenv |

## Architecture

```text
                 CloudGuard Dashboard
                    HTML / CSS / JS
                           |
                           v
                    Python Flask App
                           |
              +------------+------------+
              |                         |
              v                         v
       LaunchDarkly SDK           AI Security API
              |                         |
              v                         v
       Feature Flags             LaunchDarkly AgentControl
              |                         |
              v                         v
       Module Visibility          Agent Configuration
                                        |
                          +-------------+-------------+
                          |             |             |
                          v             v             v
                        GPT-4o       Custom Skill    Judges
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

## LaunchDarkly AgentControl Integration

CloudGuard integrates with LaunchDarkly AgentControl to manage AI behavior independently of the application code.

**Agent configuration**

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

Verify the OpenAI connection:

```powershell
python test_openai.py
```

Test the LaunchDarkly AgentControl integration:

```powershell
python test_agentcontrol.py
```

Verify application health:

```text
http://127.0.0.1:5000/api/health
```

Verify feature flag evaluations:

```text
http://127.0.0.1:5000/api/features
```

## Key Demonstration Scenarios

### 1. Feature Management

Enable or disable individual CloudGuard security modules using LaunchDarkly feature flags.

### 2. Controlled Rollouts

Demonstrate progressive rollout configurations for security capabilities using LaunchDarkly.

### 3. Customer Targeting

Use LaunchDarkly context attributes such as customer tier and geography to demonstrate targeted feature availability.

### 4. AI Configuration Management

Change the AI model, Agent instructions, and custom skills through LaunchDarkly AgentControl.

### 5. AI Security Analysis

Submit cloud security questions through the dashboard and receive AI-generated security recommendations.

### 6. AI Evaluation

Use Accuracy and Relevance Judges to evaluate AI-generated responses and review evaluation data in LaunchDarkly Monitoring.

## Important Notes

- This is a demonstration application, not a production CNAPP platform.
- Dashboard asset counts, vulnerability findings, posture scores, and threat alerts are sample data.
- Vulnerability scan endpoints simulate success and failure events; they do not execute real infrastructure scans.
- The remediation module is a demonstration capability and does not modify cloud infrastructure.
- The AI Security Analyst provides advisory recommendations and does not perform infrastructure remediation.
- OpenAI API usage is billed separately from ChatGPT subscriptions.
- Protect all API keys and LaunchDarkly SDK credentials.

## Learning Objectives

This project demonstrates practical implementation of:

- Feature management and progressive delivery
- Context-based targeting
- AI configuration management
- Agent-based AI integration
- Custom AI skills
- AI response evaluation
- Flask API integration
- Secure management of application credentials

## Repository

GitHub: https://github.com/sulavkumar/cloudguard-security-launchdarkly-demo

**CloudGuard Security – Demonstrating Feature Management and AI-powered Cloud Security.**
