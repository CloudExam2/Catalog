resource "aws_security_group" "catalog_ec2" {
  name_prefix = "catalog-service-ec2-"
  description = "HTTP and SSH for lab console connect and browser access"
  vpc_id      = data.terraform_remote_state.core.outputs.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "catalog-ec2-sg"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group" "catalog_rds" {
  name_prefix = "catalog-service-rds-"
  description = "PostgreSQL for Catalog - ingress only from Catalog EC2 SG"
  vpc_id      = data.terraform_remote_state.core.outputs.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.catalog_ec2.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "catalog-rds-sg"
  }

  lifecycle {
    create_before_destroy = true
  }
}
