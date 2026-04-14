variable "name" {
  type = string
}

variable "location" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "gateway_subnet_id" {
  description = "GatewaySubnet ID from VNet"
  type        = string
}

variable "vpn_client_address_space" {
  type = list(string)
}

variable "root_certificate_data" {
  description = "Base64 encoded root certificate"
  type        = string
}

variable "environment" {
  description = "Environment name (test/prod)"
  type        = string
}