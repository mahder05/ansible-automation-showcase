# 🚀 Platform Engineering Portfolio: Enterprise GitOps CI/CD

Welcome to the central documentation for my Platform Engineering portfolio project. This repository demonstrates a production-grade, end-to-end GitOps pipeline built entirely on a local Kubernetes cluster (Minikube). 

It showcases the evolution from a public webhook-driven architecture to a highly secure, air-gapped, and ephemeral CI/CD model utilized by enterprise platform teams.

---

## 🏗️ Architecture Overview

This platform implements a robust two-stage **Continuous Integration (CI)** and **Continuous Deployment (CD)** pipeline using **GitHub Actions** and **AWX (Ansible Tower)**.

### The Current State: Air-Gapped Enterprise GitOps
1. **Source of Truth:** Code is pushed to this GitHub repository.
2. **Event Trigger:** GitHub notifies the Actions control plane.
3. **CI (Continuous Integration):** The **Actions Runner Controller (ARC)** inside Kubernetes detects the job, spins up an ephemeral (temporary) runner pod, lints the Ansible code, and tests for syntax errors.
4. **CD (Continuous Deployment):** If CI passes, the runner communicates *internally* via Kubernetes DNS to the AWX service API. It triggers an AWX Job Template using a secure service account token. AWX spins up its own ephemeral execution environment, pulls the latest code, and deploys the infrastructure.
5. **Clean Up:** The ARC runner pod terminates automatically, scaling back to zero.

### 🛠️ Core Technologies Used
* **Kubernetes (Minikube):** The foundational container orchestration platform.
* **Helm:** Package manager used for deploying ARC.
* **AWX (Ansible Tower):** The control plane for Continuous Deployment.
* **GitHub Actions:** The control plane for Continuous Integration.
* **Actions Runner Controller (ARC):** Manages ephemeral, self-hosted CI runners natively inside Kubernetes.
* **ngrok:** (Legacy phase) Secure tunneling for webhooks.

---

## 🔒 Current Setup: Self-Hosted CI/CD with ARC (Recommended)

This is the active pipeline configuration that operates without exposing the local network to the public internet.

### 1. Deploying the Actions Runner Controller (ARC)
```bash
# Add Helm (if not installed)
brew install helm

# Install the ARC Controller
helm install arc   --namespace arc-systems   --create-namespace   oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller

# Install the Runner Scale Set
helm install portfolio-runner   --namespace arc-runners   --create-namespace   --set githubConfigUrl="https://github.com/mahder05/platform-engineering-portfolio"   --set githubConfigSecret.github_token="<YOUR_GITHUB_PAT>"   oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set
```

### 2. Generating an Internal AWX API Token
Instead of the root admin, a dedicated service account (`mbd`) is used for the pipeline.
To generate a token for internal API calls, execute this against the AWX REST API:

```bash
curl -s -X POST   -H "Content-Type: application/json"   -u mbd:<MBD_PASSWORD>   http://127.0.0.1:51688/api/v2/users/<USER_ID>/personal_tokens/   -d '{"description": "GitHub Actions Internal Token", "application": null, "scope": "write"}'
```
*Save this token in GitHub as a Repository Secret named `AWX_TOKEN`.*

### 3. Pipeline Configuration (`.github/workflows/ci.yml`)
```yaml
name: Platform CI/CD

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  pipeline:
    name: Build, Test, and Deploy
    runs-on: portfolio-runner
    
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Ansible & Linter
        run: |
          python -m pip install --upgrade pip
          pip install ansible ansible-lint

      - name: Run Ansible Lint (CI Phase)
        run: |
          ansible-lint ansible/playbooks/test-connection.yml

      - name: Trigger AWX Deployment (CD Phase)
        run: |
          echo "Triggering AWX Job Template 9 internally..."
          curl -s -X POST             -H "Authorization: Bearer ${{ secrets.AWX_TOKEN }}"             -H "Content-Type: application/json"             http://awx-service.awx.svc.cluster.local/api/v2/job_templates/9/launch/             -d '{}'
```

---

## 📡 Historical Reference: Public Webhooks via ngrok

*Note: This approach was used in Phase 1 of the project to establish initial CD connectivity before migrating to the air-gapped ARC architecture. It is documented here for future reference or if public internet routing is required in an external environment.*

### 1. Exposing Local AWX to the Internet
Because Minikube runs locally (e.g., `127.0.0.1:51688`), GitHub cannot send webhook payloads to it directly. `ngrok` creates a secure tunnel mapping a public HTTPS URL to the local cluster port.

```bash
ngrok http 51688
```
*Example Output:* `Forwarding: https://a1b2-c3d4.ngrok-free.app -> http://localhost:51688`

### 2. Configuring the GitHub Webhook
1. In AWX, enable webhooks on the target Job Template and copy the **Webhook Key**.
2. Identify the Job Template ID and construct the Payload URL:
   * **Format:** `https://<NGROK_ID>.ngrok-free.app/api/v2/job_templates/<TEMPLATE_ID>/github/`
3. In GitHub Repository -> **Settings** -> **Webhooks**:
   * **Payload URL:** Paste the constructed ngrok URL.
   * **Content Type:** `application/json` *(Crucial: AWX rejects form-urlencoded)*.
   * **Secret:** Paste the AWX Webhook Key.
   * **Events:** Pushes.

### 3. AWX Project Configuration
To ensure AWX pulls the latest code when the webhook fires, the associated AWX Project must have **"Update Revision on Launch"** enabled. This ensures the job always executes the most recent commit.

---

## 🚀 Next Steps & Roadmap
- [x] Establish base Kubernetes / AWX infrastructure.
- [x] Wire up GitHub Webhooks (Phase 1).
- [x] Deploy Actions Runner Controller (ARC) for Self-Hosted CI.
- [x] Build Air-Gapped Internal CI/CD Pipeline (Phase 2).
- [ ] Develop Ansible playbooks for actual infrastructure provisioning.
- [ ] Implement Terraform for declarative infrastructure state.

