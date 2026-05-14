resource "aws_db_subnet_group" "catalogsvc" {
  name       = "catalog-db-subnet"
  subnet_ids = data.aws_subnets.default.ids

  tags = {
    Name = "catalog-db-subnet-group"
  }
}

resource "aws_db_instance" "catalogsvc" {
  identifier                 = "catalog-postgres"
  engine                     = "postgres"
  engine_version             = "16"
  instance_class             = "db.t3.micro"
  allocated_storage          = 20
  max_allocated_storage      = 50
  storage_type               = "gp3"
  # "catalog" is reserved by RDS for PostgreSQL; use a distinct initial DB name.
  db_name                    = "catalogsvc"
  username                   = "catalogadmin"
  password                   = var.db_password
  db_subnet_group_name       = aws_db_subnet_group.catalog.name
  vpc_security_group_ids     = [aws_security_group.catalog_rds.id]
  skip_final_snapshot          = true
  publicly_accessible        = false
  backup_retention_period    = 0

  tags = {
    Name = "catalog-postgres"
  }
}
