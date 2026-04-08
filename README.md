# Pleiades

A production-style DevOps project demonstrating a full GitOps pipeline.

## Stack 
- **App**: Flash (Python) with Prometheus metrics
- **Containerization**: Docker + Docker Hub
- **CI**: GitHub Actions (auto build & push on every commit)
- **Infra**: AWS EC2 (t3.micro) via Terraform
- **Orachestration**: k3s (lightweight Kubernetes)
- **GitOps**: ArgoCD (auto-sync from this repor)
_ **Monitoring**: Prometheus + Grafana

## How it works 
1.Push code to 'main'
2.GitHub Actions builds and pushes Dockers image to Docker Hub
3.ArgoCD detects changes in 'k8s/' and syncs to the cluster automatically

## Project Structure

pleiades/
├── app/          # Flask app + Dockerfile
├── k8s/          # Kubernetes manifests
├── argocd/       # ArgoCD application config
├── terraform/    # AWS EC2 infrastructure
└── .github/      # CI pipeline

## Endpoints
- '/' -- hello message
- '/health' --health check
- '/metrics' -- Prometheus metrics
