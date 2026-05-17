output "ec2_instance_id" {
  description = "EC2 instance ID for SSM deploy and debugging"
  value       = aws_instance.catalog_service.id
}

output "catalog_public_ip" {
  description = "Public IP of the Catalog EC2 (direct HTTP tests until API Gateway exists)"
  value       = aws_instance.catalog_service.public_ip
}