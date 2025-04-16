resource "kubernetes_namespace" "ingress-controller_ns" {
    metadata {
      name = "ingress-controller"
    }
  
}


resource "helm_release" "ingress-controller" {
  chart      = "nginx-ingress"
  name       = "nginx-ingress"
  namespace  = "ingress-controller"
  repository = "https://helm.nginx.com/stable/"
  version    = "2.0.0"

  values = [file("${path.module}/ingress.yml")]
}



