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

The `GitOps Delivery` workflow validates changes on pull requests. On `main`,
it synchronizes the exact commit, waits for a healthy application, and prints
application status, deployment history, managed resources, and recent pod logs
in the GitHub Actions run.

For a private Argo CD endpoint, change the deploy job to an online ephemeral
self-hosted runner with network access to Argo CD. Keep validation on the
GitHub-hosted runner.
