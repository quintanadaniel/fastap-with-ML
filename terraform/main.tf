provider "aws" {
  region = "eu-north-1"
}

resource "aws_eks_cluster" "cluster-im-det" {
  name     = "cluster-im-det"
  role_arn = "arn:aws:iam::262520292671:role/kube_role"
  vpc_config {
    subnet_ids = ["subnet-04b246e72d57e052c", "subnet-0341e161613eed3f0"]
  }
}

resource "aws_eks_node_group" "image-detector-node-group" {
  cluster_name    = "aws_eks_cluster.cluster-im-det.cluster-im-det"
  node_group_name = "image-detector-node-group"
  node_role_arn   = "arn:aws:iam::262520292671:role/kube_role"
  subnet_ids      = ["subnet-04b246e72d57e052c", "subnet-0341e161613eed3f0"]

  scaling_config {
    desired_size = 3
    max_size     = 2
    min_size     = 1
  }

  instance_types = ["t3.medium"]

  remote_access {
    ec2_ssh_key = "cluster_test"
    source_security_group_ids = ["sg-0a3bb701c5778b646","sg-04ca14b29d4b21299"]
  }

}