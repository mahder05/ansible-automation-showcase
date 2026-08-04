# Platform Engineering Portfolio: GitOps, IaC, and Air-Gapped CI/CD

This repository serves as a comprehensive showcase of modern Platform Engineering principles. It demonstrates the ability to architect, provision, and configure enterprise-grade infrastructure locally using Kubernetes, Terraform, Ansible, and GitHub Actions.

## 🏗 Architecture & Tech Stack

This project simulates a secure, air-gapped internal developer platform (IDP) similar to those found in Fortune 500 environments. 

*   **Compute Engine:** Local Kubernetes (Minikube)
*   **Infrastructure as Code (IaC):** Terraform (`hashicorp/kubernetes` provider)
*   **Configuration Management:** Ansible + AWX (Ansible Tower)
*   **CI/CD Orchestration:** GitHub Actions via Actions Runner Controller (ARC)
*   **Runner Environment:** Ephemeral, self-hosted, scale-to-zero Docker containers
*   **Version Control:** Git & GitHub

---

## 🚀 Project Phases & Implementation Steps

### Phase 1: Cluster Provisioning & Base Infrastructure
Instead of relying on costly public clouds, this environment leverages a local Minikube cluster to simulate a datacenter.
*   Deployed Minikube to act as the primary orchestration engine.
*   Configured namespaces to isolate CI/CD tools from application workloads.

### Phase 2: Secure CI/CD Pipeline (Actions Runner Controller)
To mimic an air-gapped, highly secure enterprise network, public GitHub runners were bypassed.
*   Deployed **Actions Runner Controller (ARC)** into the Minikube cluster via Helm.
*   Configured **Ephemeral Self-Hosted Runners** that dynamically scale out based on queue demand.
*   *Architecture Decision:* Tuned `minRunners` parameters to balance "Cold Start" latency against optimal resource utilization (Scale-to-Zero vs. Warm Pools).

### Phase 3: Configuration Management (Ansible & AWX)
Implemented a robust configuration management strategy using AWX (the upstream project for RedHat Ansible Automation Platform).
*   Deployed the AWX Operator and instance into Minikube.
*   Created an NGINX configuration playbook (`setup-nginx.yml`) utilizing **Jinja2 Templating**.
*   Injected dynamic variables (`environment_tier`, `server_name`) to generate environment-specific configurations at runtime.
*   Enforced strict code quality by integrating `ansible-lint` to catch legacy YAML syntax (e.g., boolean truthy values) and enforce strict pathing rules for `templates/`.

### Phase 4: Infrastructure as Code (Terraform)
Adopted a declarative approach to infrastructure provisioning.
*   Managed Terraform versions using `tfenv` to align with enterprise multi-project workflows.
*   Authored HCL (`main.tf`) utilizing the HashiCorp Kubernetes Provider to authenticate securely via `~/.kube/config`.
*   Provisioned a dedicated `portfolio-apps` namespace, a highly-available 2-replica NGINX Deployment, and a NodePort Service to expose the application.
*   *Security & GitOps Hygiene:* Implemented a strict `.gitignore` to prevent Terraform state files (`.tfstate`) and massive provider binaries from leaking into version control.

### Phase 5: The Continuous Integration / Continuous Deployment Pipeline
Tied all components together using a GitHub Actions workflow (`ci.yml`) tailored for the self-hosted environment.
*   **CI Phase (Validation):** 
    *   Executes `ansible-lint` against configuration playbooks.
    *   Executes `terraform fmt -check` and `terraform validate` to ensure structural integrity of IaC.
    *   *Troubleshooting:* Disabled the HashiCorp Node.js wrapper (`terraform_wrapper: false`) to ensure compatibility with the lightweight, Node-less Alpine runner containers.
*   **CD Phase (Deployment):** 
    *   Secured communication between the ephemeral runner and AWX via Kubernetes internal DNS (`awx-service.awx.svc.cluster.local`).
    *   Triggered dynamic AWX Job Templates programmatically using internal REST API calls and secure Bearer tokens stored in GitHub Secrets.

---

## 🛠 Notable Technical Challenges Conquered
1.  **Git Divergence:** Successfully resolved split branch histories utilizing rebase/merge strategies.
2.  **Linter Strictness:** Overcame `[yaml[truthy]]` and `[template-basedir]` strict enforcement by adhering strictly to Ansible Galaxy file structure standards.
3.  **Ephemeral Runner Dependencies:** Diagnosed and bypassed Exit Code 127 errors caused by missing global binary dependencies in lightweight container environments.
4.  **State Management:** Cleaned tracking history to remove massive 50MB+ provider binaries and sensitive `.tfstate` files, establishing proper GitOps practices.

---

## 📈 Next Steps (Future Roadmap)
*   **Observability:** Introduce Prometheus and Grafana for cluster metric scraping and dashboarding.
*   **True GitOps:** Replace the API-driven CD pipeline with ArgoCD for continuous reconciliation.
