variable "aws_region" {
  type        = string
  description = "AWS region for all resources"
  default     = "us-east-1"
}

variable "github_token" {
  description = "GitHub Personal Access Token"
  type        = string
  sensitive   = true
}

variable "github_owner" {
  description = "GitHub username or organization"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name (short name; owner comes from provider)"
  type        = string
}

variable "catalog_backend_url" {
  description = "The URL for the Catalog backend service (e.g., http://IP:80). Set this to the Catalog EC2 instance's public IP after deployment. This is used by Core to proxy requests to Catalog."
  type        = string
  default     = ""
}