module "networking" {
  source = "../../../modules/networking"

  location              = var.location
  resource_group_name   = var.resource_group_name
  environment_name      = var.environment_name
  vnet_cidr             = var.vnet_cidr
  public_subnet_cidr    = var.public_subnet_cidr
  private_subnet_cidr   = var.private_subnet_cidr
  developer_ip          = var.developer_ip
  gateway_subnet_cidr   = var.gateway_subnet_cidr
}