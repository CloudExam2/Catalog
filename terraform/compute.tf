resource "aws_instance" "catalog_service" {
  ami                    = "ami-0440d3b780d96b29d" # Amazon Linux 2023 (us-east-1)
  instance_type          = "t2.micro"
  subnet_id              = data.terraform_remote_state.core.outputs.public_subnet_ids[0]
  iam_instance_profile   = "LabInstanceProfile"
  vpc_security_group_ids = [aws_security_group.catalog_ec2.id]

  user_data = <<-EOF
              #!/bin/bash
              set -e
              dnf update -y
              dnf install -y docker
              systemctl enable --now docker
              ACCOUNT_ID=${data.aws_caller_identity.current.account_id}
              aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.${var.aws_region}.amazonaws.com
              docker pull $ACCOUNT_ID.dkr.ecr.${var.aws_region}.amazonaws.com/catalog-service:latest || true
              docker system prune -af || true
              docker image prune -af || true
              docker stop catalog-app 2>/dev/null || true 
              docker rm catalog-app 2>/dev/null || true
              docker run -d --name catalog-app -p 80:8000 \
                $ACCOUNT_ID.dkr.ecr.${var.aws_region}.amazonaws.com/catalog-service:latest
              EOF

  tags = {
    Name      = "Catalog-Service"
    ManagedBy = "terraform-catalog"
  }
}

resource "aws_eip" "catalog" {
  domain = "vpc"
  tags = {
    Name      = "catalog-service-eip"
    ManagedBy = "terraform-catalog"
  }
}

resource "aws_eip_association" "catalog" {
  instance_id   = aws_instance.catalog_service.id
  allocation_id = aws_eip.catalog.id
}

resource "github_actions_secret" "ec2_catalog_id" {
  repository      = var.github_repo
  secret_name     = "EC2_CATALOG_ID"
  plaintext_value = aws_instance.catalog_service.id
}

resource "github_actions_variable" "catalog_url_for_core" {
  provider      = github.core
  repository    = "Core"
  variable_name = "CATALOG_BACKEND_URL"
  value         = "http://${aws_eip.catalog.public_ip}:80"
}
