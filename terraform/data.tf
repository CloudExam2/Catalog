data "aws_caller_identity" "current" {}

data "aws_ecr_repository" "catalog" {
  name = "catalog-service"
}
