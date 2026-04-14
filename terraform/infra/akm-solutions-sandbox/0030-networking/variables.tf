variable "location" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "environment_name" {
  type = string
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
  description = "CIDR block for GatewaySubnet"
  type        = string
}