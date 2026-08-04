Complete Platform Engineering Journey
From Local Cluster to Air-Gapped GitOps & IaC
A comprehensive master guide detailing every step, concept, and configuration used to build this enterprise-grade platform.
Phase 1: Foundation & Local Orchestration
1.1 Provisioning the Kubernetes Cluster (Minikube)
To simulate an enterprise datacenter without incurring cloud costs, we initialized a local Kubernetes cluster using Minikube.
⚬	Started the cluster with sufficient resources (CPU/Memory).
⚬	Created dedicated namespaces to separate our tooling (CI/CD, AWX) from our actual applications (portfolio-apps).
Phase 2: Secure CI/CD (Actions Runner Controller)
2.1 Bypassing Public Runners
In secure enterprise environments, code cannot leave the private network to run on public GitHub servers. We deployed Actions Runner Controller (ARC) via Helm to host our own runners inside Kubernetes.
2.2 Ephemeral, Scale-to-Zero Architecture
We configured an ephemeral runner class (portfolio-runner). This means when a GitHub Action triggers, a brand-new Docker container boots up, authenticates via a GitHub token, processes the job, and destroys itself. We initially configured minRunners=0 to save resources, accepting a slight "Cold Start" delay.
Phase 3: Configuration Management (AWX & Ansible)
3.1 Deploying AWX
We deployed AWX (the open-source upstream for Red Hat Ansible Automation Platform) into the cluster. AWX provides a UI, RBAC (Role-Based Access Control), and API endpoints to manage Ansible playbooks.
3.2 Dynamic Jinja2 Templating
Instead of hardcoding HTML files, we utilized Jinja2 templates to inject dynamic variables into our configurations. We created an index.html.j2 template:
<h1>Welcome to Mahder's GitOps Server!</h1>
<p>Environment: <strong>{{ environment_tier | upper }}</strong></p>
<p>Deployed by: <strong>GitHub Actions + AWX</strong></p>

We wrote setup-nginx.yml to process this template and generate the final configuration file on the target nodes.
Phase 4: Enforcing Enterprise Standards
4.1 Ansible Linting & strict YAML
Before allowing code into the main branch, we ran ansible-lint. It immediately caught two legacy practices:
⚬	Truthy values: We changed gather_facts: yes to the strict boolean gather_facts: true.
⚬	Directory strictness: We moved our template file into a playbooks/templates/ directory. Ansible natively auto-discovers the templates/ folder, allowing us to remove relative paths (../) from the playbook.
4.2 Resolving Git Divergence
While syncing local changes with the remote GitHub repository, we encountered a divergent branch warning. We configured Git to merge histories cleanly:
git config pull.rebase false
git pull origin main
git push

Phase 5: Infrastructure as Code (Terraform)
5.1 Version Management with tfenv
Because different projects require different Terraform versions, we bypassed Homebrew's default Terraform installation and used tfenv (a version manager) to install the CLI.
5.2 Writing HCL (HashiCorp Configuration Language)
We created a terraform folder and wrote main.tf. This code authenticates directly to the Minikube cluster using our local ~/.kube/config and provisions:
⚬	A dedicated portfolio-apps namespace.
⚬	A highly available 2-replica NGINX Deployment.
⚬	A NodePort Service to route traffic to the pods.
We executed the standard IaC lifecycle locally: terraform init, terraform plan, and terraform apply -auto-approve.
Phase 6: Pipeline Integration & Troubleshooting
6.1 Updating the CI/CD Pipeline
We updated our GitHub Actions workflow (ci.yml) to include Terraform validation (fmt -check and validate) alongside our Ansible linting. The pipeline concludes by hitting the internal AWX REST API to trigger the deployment (CD Phase).
6.2 Managing Large Binaries and State Files
The Problem: When pushing the Terraform code, GitHub warned of a 50MB+ file. We accidentally committed the massive .terraform provider plugin directory and our sensitive terraform.tfstate file.
The Fix: We created a .gitignore file and removed the tracked files from Git's cache without deleting them locally:
cd root_directory
git rm -r --cached terraform/.terraform
git rm --cached terraform/terraform.tfstate
git add .
git commit -m "chore: Removed Terraform state from tracking"
git push

6.3 Exit Code 127 (Node.js Missing on Runner)
The Problem: The CI pipeline crashed on the "Set up Terraform" step. HashiCorp's GitHub Action attempts to install a Node.js wrapper to capture outputs, but our lightweight Alpine runner container didn't have Node.js installed.
The Fix: We passed a parameter to disable the wrapper entirely in ci.yml:
- name: Set up Terraform
  uses: hashicorp/setup-terraform@v3
  with:
    terraform_wrapper: false

6.4 Cold Starts vs. Warm Pools
We analyzed why pipeline jobs sat in the queue before executing. Our minRunners=0 ARC setup caused a 30-second "Cold Start" as Kubernetes provisioned a pod from scratch. We documented that upgrading the Helm release to minRunners=1 creates a "Warm Pool" for instant execution, trading CPU efficiency for pipeline speed.
