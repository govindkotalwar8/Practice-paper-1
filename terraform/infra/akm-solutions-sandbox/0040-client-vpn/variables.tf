variable "location" {}
variable "resource_group_name" {}

variable "vpn_client_address_space" {
  type = list(string)
}

variable "environment" {
  type = string
}
variable "root_certificate_data" {
  type      = string
  sensitive = true
}