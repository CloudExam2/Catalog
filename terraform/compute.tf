resource "aws_instance" "catalog_service" {
  ami                    = "ami-0440d3b780d96b29d" # Amazon Linux 2023 (us-east-1)
  instance_type          = "t2.micro"
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
              docker stop catalog-app 2>/dev/null || true
              docker rm catalog-app 2>/dev/null || true
              docker run -d --name catalog-app -p 80:8000 \
                $ACCOUNT_ID.dkr.ecr.${var.aws_region}.amazonaws.com/catalog-service:latest
              EOF

  tags = {
    Name = "Catalog-Service"
  }
}

resource "github_actions_secret" "ec2_instance_id" {
  repository      = var.github_repo
  secret_name     = "EC2_INSTANCE_ID"
  plaintext_value = aws_instance.catalog_service.id
}

resource "github_actions_secret" "catalog_database_url" {
  repository      = var.github_repo
  secret_name     = "CATALOG_DATABASE_URL"
  plaintext_value = "postgresql://catalogadmin:${var.db_password}@${aws_db_instance.catalog.address}:5432/catalogsvc"
}
