resource "aws_security_group" "catalog_ec2" {
  name        = "catalog-service-ec2-sg"
  description = "Allow SSH and HTTP from your IP only (student lab; same pattern as Sales)"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["189.163.24.169/32"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["189.163.24.169/32"]
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
}

resource "aws_security_group" "catalog_rds" {
  name        = "catalog-service-rds-sg"
  description = "PostgreSQL for Catalog - ingress only from Catalog EC2 SG"

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
}
