output "ec2_instance_id" {
  description = "EC2 instance ID for SSM deploy and debugging"
  value       = aws_instance.catalog_service.id
}

output "catalog_public_ip" {
  description = "Public IPv4 of Catalog EC2 (use with http:// below)"
  value       = aws_instance.catalog_service.public_ip
}