# DB subnet group in the Core VPC only. Use a *new* AWS name so Terraform never tries to
# "ModifyDBSubnetGroup" across VPCs (that returns InvalidParameterValue).
resource "aws_db_subnet_group" "catalog_core" {
  name       = "catalog-db-subnet-core-vpc"
  subnet_ids = data.terraform_remote_state.core.outputs.public_subnet_ids

  tags = {
    Name = "catalog-db-subnet-group-core"
  }
}

# New identifier => replacement when moving from default VPC to Core VPC (old instance must go first).
resource "aws_db_instance" "catalog" {
  identifier              = "catalog-postgres-core"
  engine                  = "postgres"
  engine_version          = "16"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  max_allocated_storage   = 50
  storage_type            = "gp3"
  db_name                 = "catalogsvc"
  username                = "catalogadmin"
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.catalog_core.name
  vpc_security_group_ids  = [aws_security_group.catalog_rds.id]
  skip_final_snapshot     = true
  publicly_accessible     = false
  backup_retention_period = 0
  apply_immediately       = true

  tags = {
    Name = "catalog-postgres-core"
  }
}
