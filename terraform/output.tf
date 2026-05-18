output "ec2_catalog_id" {
  description = "EC2 instance ID for SSM deploy and debugging"
  value       = aws_instance.catalog_service.id
}

output "catalog_public_ip" {
  description = "Stable public IPv4 (Elastic IP) for Catalog"
  value       = aws_eip.catalog.public_ip
}

output "catalog_backend_url" {
  description = "Base URL written to Core CATALOG_BACKEND_URL"
  value       = "http://${aws_eip.catalog.public_ip}:80"
}