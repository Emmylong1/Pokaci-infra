module "eks" {
  source                        = "../../module/eks"
  env                           = "stagings"
  is_eks_role_enabled           = true
  is_eks_nodegroup_role_enabled = true
  cidr-block                    = "10.0.0.0/16"
  vpc-name                      = "vpc"
  igw-name                      = "igw"
  pub-subnet-count              = 3
  pub-cidr-block                = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  pub-availability-zone         = ["us-east-1a", "us-east-1b", "us-east-1c"]
  pub-sub-name                  = "subnet-public"
  pri-subnet-count              = 3
  pri-cidr-block                = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  pri-availability-zone         = ["us-east-1a", "us-east-1b", "us-east-1c"]
  pri-sub-name                  = "subnet-private"
  public-rt-name                = "public-route-table"
  private-rt-name               = "private-route-table"
  eip-name                      = "elasticip-ngw"
  ngw-name                      = "ngw"
 eks-sg                        = "eks-sg"

  # EKS
  is-eks-cluster-enabled     = true
  cluster-version            = "1.29"
  cluster-name               = "eks-cluster"
  endpoint-private-access    = true
  endpoint-public-access     = true
  ondemand_instance_types    = ["t2.small"]
  spot_instance_types        = ["t2.small", "t2.small", "t2.small", "t2.small", "t2.small", "t2.small", "t2.small", "t2.small", "t2.small"]
  desired_capacity_on_demand = "1"
  min_capacity_on_demand     = "1"
  max_capacity_on_demand     = "5"
  desired_capacity_spot      = "1"
  min_capacity_spot          = "1"
  max_capacity_spot          = "10"
  ssh_key_name               = "testkey"
  addons = [
    {
      name    = "vpc-cni",
      version = "v1.18.1-eksbuild.1"
    },
    {
      name    = "coredns"
      version = "v1.11.1-eksbuild.9"
    },
    {
      name    = "kube-proxy"
      version = "v1.29.3-eksbuild.2"
    },
    {
      name    = "aws-ebs-csi-driver"
      version = "v1.30.0-eksbuild.1"
    }
  ]
}


module "ingress-controller" {
 source     = "../../module/ingress-controller/helm-chart-values"
}

module "argocd" {
source     = "../../module/argocd"
depends_on = [module.ingress-controller]
}


#module "prometheus" {
# source     = "../../modules/prometheus/helm-chart-values"
# depends_on = [module.ingress-controller]
#}

#module "grafana" {
# source     = "../../modules/grafana/helm-chart-values"
#depends_on = [module.ingress-controller]
#}