# EC2 + EIP + GitHub wiring (scripts live in ./compute/)

resource "aws_instance" "catalog_service" {
  ami                    = "ami-0440d3b780d96b29d" # Amazon Linux 2023 (us-east-1)
  instance_type          = "t2.micro"
  subnet_id              = data.terraform_remote_state.core.outputs.public_subnet_ids[0]
  iam_instance_profile   = "LabInstanceProfile"
  vpc_security_group_ids = [aws_security_group.catalog_ec2.id]

  user_data = base64encode(templatefile("${path.module}/compute/user_data.sh.tpl", {
    aws_region        = var.aws_region
    account_id        = data.aws_caller_identity.current.account_id
    ecr_repo          = "catalog-service"
    docker_script     = indent(2, templatefile("${path.module}/compute/docker.sh.tpl", {
      aws_region = var.aws_region
      account_id = data.aws_caller_identity.current.account_id
      ecr_repo   = "catalog-service"
    }))
    cloudwatch_script = indent(2, templatefile("${path.module}/compute/cloudwatch.sh.tpl", {
      cw_config = templatefile("${path.module}/compute/cloudwatch_agent.json.tpl", {
        log_group_name = data.terraform_remote_state.core.outputs.catalog_log_group_name
      })
    }))
  }))

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
