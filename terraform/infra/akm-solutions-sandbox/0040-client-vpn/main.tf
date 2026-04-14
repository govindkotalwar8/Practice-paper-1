data "terraform_remote_state" "networking" {
  backend = "azurerm"

  config = {
    resource_group_name  = "experimental-govind-kotalwar"
    storage_account_name = "govindstate12345"
    container_name       = "tfstate"
    key                  = "sandbox-networking.tfstate"
  }
}

module "client_vpn" {
  source = "../../../modules/client-vpn"

  name                = "clientvpn"
  location            = var.location
  resource_group_name = var.resource_group_name

  environment               = var.environment
  gateway_subnet_id        = data.terraform_remote_state.networking.outputs.gateway_subnet_id
  vpn_client_address_space = var.vpn_client_address_space
  root_certificate_data    = var.root_certificate_data
}