# 🚀 Platform Engineering & GitOps Portfolio

![Ansible](https://img.shields.io/badge/Ansible-AWX-EE0000?style=for-the-badge&logo=ansible&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![GitOps](https://img.shields.io/badge/GitOps-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

## 📌 Overview
This repository serves as the central **Control Plane** for an enterprise-grade Platform Engineering and GitOps workflow. It demonstrates a unified approach to Infrastructure as Code (IaC), Configuration Management, and Container Orchestration. 

By leveraging **AWX (Ansible Automation Platform)** running on **Kubernetes**, this architecture allows for zero-touch provisioning, immutable infrastructure, and automated lifecycle management.

---

## 🏗️ Architecture & Tech Stack
* **Configuration Management:** Ansible / AWX
* **Infrastructure as Code (IaC):** Terraform
* **Container Orchestration:** Kubernetes (Minikube / Helm)
* **Source of Truth (GitOps):** GitHub
* **Execution Environment:** Containerized Ansible Runner Pods (awx-ee)

---

## 📂 Enterprise Repository Structure
This repository follows an industry-standard mono-repo structure, separating concerns across the infrastructure lifecycle:

```text
.
├── ansible/
│   ├── inventory/         # Dynamic and static inventory definitions
│   ├── playbooks/         # Core automation and configuration playbooks
│   └── roles/             # Modular, reusable Ansible roles
├── kubernetes/
│   └── manifests/         # K8s deployments, services, and GitOps state files
├── terraform/
│   ├── environments/      # State isolation for Dev, Staging, and Prod
│   └── modules/           # Reusable Terraform resource modules
└── .github/
    └── workflows/         # CI/CD pipelines for linting and deployment
