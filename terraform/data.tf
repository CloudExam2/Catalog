data "aws_caller_identity" "current" {}

# ECS-optimized Amazon Linux 2 includes Docker; avoids dnf to the public internet when VPC has no IGW.
data "aws_ssm_parameter" "ecs_optimized_ami" {
  name = "/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id"
}

data "aws_ecr_repository" "catalog" {
  name = "catalog-service"
}
