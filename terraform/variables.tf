variable "kubeconfig_path" {
  description = "Path to the kubeconfig file."
  type        = string
  default     = "~/.kube/config"
}

variable "kubeconfig_context" {
  description = "Kubernetes context used by the provider."
  type        = string
  default     = "minikube"
}

variable "namespace" {
  description = "Namespace for the example workload."
  type        = string
  default     = "portfolio-apps"
}

variable "replicas" {
  description = "Number of NGINX replicas."
  type        = number
  default     = 2

  validation {
    condition     = var.replicas >= 1
    error_message = "replicas must be at least 1."
  }
}
