# Ansible Automation Showcase

This repository contains practical examples of infrastructure automation with
Ansible, Kubernetes, Argo CD, Terraform, and GitHub Actions.

## What is included

- Ansible playbooks and roles for Linux administration
- An AWX deployment example
- Kubernetes manifests for a sample application
- An Argo CD project and application
- Terraform and Docker lab examples
- A GitHub Actions workflow for manifest validation and Argo CD deployment

## Repository layout

```text
ansible/       Ansible inventory, playbooks, roles, and requirements
argocd/        Argo CD project, application, and setup instructions
gitops/        Kubernetes workloads managed by Argo CD
terraform/     Terraform examples
devops-labs/   Docker and AWX lab files
```

## GitOps workflow

Changes to `argocd/` or `gitops/` trigger the GitHub Actions workflow. Pull
requests validate the manifests. Changes merged into `main` are synchronized
through Argo CD, and the workflow displays deployment status, resource details,
history, and recent application logs.

Before deployment, create a GitHub environment named `production` and configure
the `ARGOCD_SERVER` and `ARGOCD_AUTH_TOKEN` secrets. Follow the bootstrap steps
in [argocd/README.md](argocd/README.md).

## Running Ansible locally

Install the required collections:

```bash
ansible-galaxy collection install -r ansible/requirements.yml
```

Run a connectivity check:

```bash
ansible-playbook -i ansible/inventory.ini ansible/playbooks/test-connection.yml
```

Review the inventory and playbooks before running them against your own hosts.

## License

This project is available under the MIT License.
