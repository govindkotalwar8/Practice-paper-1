resource "azurerm_public_ip" "vpn_pip" {
  name                = "${var.name}-vpn-pip"
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"

  zones = ["1", "2", "3"] 

  tags = {
    environment = var.environment
  }
}

resource "azurerm_virtual_network_gateway" "vpn_gateway" {
  name                = "${var.name}-vpn-gateway"
  location            = var.location
  resource_group_name = var.resource_group_name

  type     = "Vpn"
  vpn_type = "RouteBased"

  active_active = false
  bgp_enabled   = false
  sku           = "VpnGw1AZ"

  depends_on = [azurerm_public_ip.vpn_pip]

  tags = {
    environment = var.environment
  }

  ip_configuration {
    name                          = "vnetGatewayConfig"
    public_ip_address_id          = azurerm_public_ip.vpn_pip.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = var.gateway_subnet_id
  }

  vpn_client_configuration {
    address_space = var.vpn_client_address_space

    vpn_client_protocols = ["OpenVPN"]

    root_certificate {
      name             = "root-cert"
      public_cert_data = var.root_certificate_data
    }
  }
}