resource "kubernetes_namespace" "argocd_ns" {
    metadata {
      name = "argocd"
    }
  
}


resource "helm_release" "argocd_ns" {
  chart      = "argo-cd"
  name       = "argocd"
  namespace  = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  version    = "7.8.26"

  values = [file("${path.module}/argocd.yml")]
}



