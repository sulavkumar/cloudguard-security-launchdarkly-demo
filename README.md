
# CloudGuard Security – LaunchDarkly Demo

An enterprise-style Cloud-Native Application Protection Platform (CNAPP) dashboard demonstrating LaunchDarkly feature management capabilities using Python, Flask, and the LaunchDarkly Server-Side SDK.

## Project Overview

CloudGuard Security is a simulated enterprise security dashboard designed to demonstrate how organizations can manage feature availability, target customers, and progressively release new capabilities using LaunchDarkly.

The dashboard uses sample security data and simulated vulnerability scan events.

## Technology Stack

- Python
- Flask
- LaunchDarkly Python Server-Side SDK
- HTML, CSS and JavaScript
- Git and GitHub

## Features

### 1. Feature Flags

Five LaunchDarkly Boolean flags control dashboard capabilities:

- `new_security_dashboard`
- `advanced_vulnerability_scanning`
- `threat_detection_enabled`
- `auto_remediation_enabled`
- `ai_security_assistant`

### 2. Customer Targeting

Demonstrates customer-level feature targeting using LaunchDarkly context attributes.

Example:
- Premium customers: AI Security Analyst enabled.
- Standard customers: AI Security Analyst disabled.

### 3. Progressive Rollouts

Demonstrates controlled feature releases:

- 10% rollout
- 50% rollout
- 100% rollout

### 4. Custom Metrics and Event Tracking

CloudGuard sends simulated vulnerability scan events to LaunchDarkly.

Events:
- `vulnerability_scan_success`
- `vulnerability_scan_failure`

Custom metrics:
- CloudGuard Vulnerability Scan Success Rate
- CloudGuard Vulnerability Scan Failure Rate

### 5. Simulated Vulnerability Scan APIs

Successful scan:

`GET /api/scan/success`

Failed scan:

`GET /api/scan/failure`

Feature evaluation:

`GET /api/features`

Application health:

`GET /api/health`

## Project Structure

```text
cloudguard-security/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## Local Setup

### Prerequisites

- Python 3.10 or later
- Git
- LaunchDarkly account and Test environment

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/cloudguard-security-launchdarkly-demo.git
cd cloudguard-security-launchdarkly-demo
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure LaunchDarkly

Copy `.env.example` to `.env`.

Add your LaunchDarkly Server-Side SDK key to `.env`:

```text
LAUNCHDARKLY_SDK_KEY=your-server-side-sdk-key
```

Never commit your `.env` file or expose your SDK key.

### 5. Start CloudGuard

```powershell
python app.py
```

Open:

`http://127.0.0.1:5000`

## Important Notes

- This is a demonstration application, not a production CNAPP solution.
- Dashboard security findings and asset information are sample data.
- Vulnerability scan endpoints simulate success and failure events; they do not perform real security scans.
- The application demonstrates feature visibility, not production authorization or security enforcement.
- Guarded rollouts and automatic rollback have not been implemented or validated in this demo.

## Learning Objectives

This project demonstrates practical understanding of:

- Feature flag lifecycle management
- Customer segmentation and targeting
- Progressive feature delivery
- LaunchDarkly SDK integration
- Custom event tracking and metrics
- Enterprise feature release strategies

## Author

Sulav Kumar
