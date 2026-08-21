output "namespace" {
  description = "Namespace containing the example workload."
  value       = kubernetes_namespace_v1.portfolio.metadata[0].name
}

output "access_command" {
  description = "Command that forwards the NGINX service to localhost:8080."
  value       = "kubectl -n ${kubernetes_namespace_v1.portfolio.metadata[0].name} port-forward service/${kubernetes_service_v1.nginx.metadata[0].name} 8080:80"
}
