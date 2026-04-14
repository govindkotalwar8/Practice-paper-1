variable "location" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "environment_name" {
  description = "Environment name (dev, test, prod)"
  type        = string
}

variable "vnet_cidr" {
  type = list(string)
}

variable "public_subnet_cidr" {
  type = list(string)
}

variable "private_subnet_cidr" {
  type = list(string)
}

variable "developer_ip" {
  type = list(string)
}

variable "gateway_subnet_cidr" {
  description = "CIDR for Gateway Subnet"
  type        = string
}