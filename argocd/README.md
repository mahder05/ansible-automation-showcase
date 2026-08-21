# Argo CD bootstrap and GitHub Actions delivery

The files in this directory define the Argo CD project and application. They
are the one-time bootstrap layer; Argo CD manages the workload under
`gitops/hello-world` after bootstrap.

## Prerequisites

- Argo CD 3.4.x is installed in the `argocd` namespace.
- The Argo CD API is reachable from the selected GitHub Actions runner.
- The Argo CD repository-server can reach this Git repository.
- The GitHub `production` environment is restricted to the `main` branch and,
  where appropriate, protected by required reviewers.

## Bootstrap

Apply the project before the application:

```bash
kubectl apply -f argocd/project.yaml
kubectl apply -f argocd/hello-world-application.yaml
```

Confirm that Argo CD registered the application:

```bash
argocd app get hello-world
```

## Create the least-privilege automation token

The `portfolio` project declares a `github-actions` role that can only read,
sync, and retrieve logs for `portfolio/hello-world`. Apply the project before
creating its token:

```bash
kubectl apply -f argocd/project.yaml
```

Log in to Argo CD with an administrative account. For a local lab, use a
temporary port-forward in one terminal:

```bash
kubectl -n argocd port-forward svc/argocd-server 8080:443
```

Then log in from another terminal:

```bash
argocd login localhost:8080 --username admin --insecure
```

Generate a project-role token with a finite lifetime and pipe it directly to
the GitHub environment secret so it is not printed or stored in the repository:

```bash
argocd proj role create-token portfolio github-actions \
  --id github-actions-$(date +%Y-%m) \
  --expires-in 720h \
  --token-only | \
gh secret set ARGOCD_AUTH_TOKEN \
  --env production \
  --repo mderangula/ansible-automation-showcase
```

Rotate this 30-day token before it expires. After confirming the replacement
works, list and remove the expired token from the project role:

```bash
argocd proj role list-tokens portfolio github-actions
argocd proj role delete-token portfolio github-actions TOKEN_ID
```

## GitHub environment configuration

Create a GitHub environment named `production` and add these environment
secrets:

- `ARGOCD_SERVER`: the reachable Argo CD API hostname, without credentials.
- `ARGOCD_AUTH_TOKEN`: a dedicated automation token limited to synchronizing
  and reading the `portfolio/hello-world` application.

Optional environment variable:

- `ARGOCD_INSECURE=true`: only for lab environments using an untrusted TLS
  certificate. Production should use a trusted certificate and leave this
  unset or `false`.

Set the server without putting a credential in shell history:

```bash
printf '%s' 'argocd.example.com:443' | \
gh secret set ARGOCD_SERVER \
  --env production \
  --repo mderangula/ansible-automation-showcase
```

Confirm that the names exist; GitHub will not display their values:

```bash
gh secret list \
  --env production \
  --repo mderangula/ansible-automation-showcase
```

The `GitOps Delivery` workflow validates changes on pull requests. On `main`,
it synchronizes the tracked branch, waits for a healthy application, verifies
that Argo CD deployed the triggering commit SHA, and prints application status,
deployment history, managed resources, and recent pod logs in the Actions run.

GitHub-hosted runners cannot reach a workstation port-forward, Kubernetes
`ClusterIP`, `.local` hostname, or private LAN address. Manifest validation
therefore remains on a GitHub-hosted runner, while the deployment job requires
a macOS ARM64 self-hosted runner with the `argocd` and `orbstack` labels. The
deployment job creates and cleans up its own local port-forward. Set
`ARGOCD_SERVER` to `localhost:8080` for this lab topology.
