terraform {
  backend "azurerm" {
    resource_group_name  = "experimental-govind-kotalwar"
    storage_account_name = "govindstate12345"
    container_name       = "tfstate"
    key                  = "sandbox-backend.tfstate"
  }
}