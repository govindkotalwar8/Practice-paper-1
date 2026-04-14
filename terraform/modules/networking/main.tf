# VNet
resource "azurerm_virtual_network" "this" {
  name                = var.environment_name
  address_space       = var.vnet_cidr
  location            = var.location
  resource_group_name = var.resource_group_name
}

# Subnets
resource "azurerm_subnet" "public" {
  name                 = "public-${var.environment_name}"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = var.public_subnet_cidr
}

resource "azurerm_subnet" "private" {
  name                 = "private-${var.environment_name}"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = var.private_subnet_cidr
}

# NAT
resource "azurerm_public_ip" "nat" {
  name                = "nat-${var.environment_name}"
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_nat_gateway" "this" {
  name                = var.environment_name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku_name            = "Standard"
}

resource "azurerm_nat_gateway_public_ip_association" "this" {
  nat_gateway_id       = azurerm_nat_gateway.this.id
  public_ip_address_id = azurerm_public_ip.nat.id
}

resource "azurerm_subnet_nat_gateway_association" "this" {
  subnet_id      = azurerm_subnet.private.id
  nat_gateway_id = azurerm_nat_gateway.this.id
}

# NSG (NO RULES HERE)
resource "azurerm_network_security_group" "public" {
  name                = "public-${var.environment_name}"
  location            = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_network_security_group" "private" {
  name                = "private-${var.environment_name}"
  location            = var.location
  resource_group_name = var.resource_group_name
}

# Attach NSG
resource "azurerm_subnet_network_security_group_association" "public" {
  subnet_id                 = azurerm_subnet.public.id
  network_security_group_id = azurerm_network_security_group.public.id
}

resource "azurerm_subnet_network_security_group_association" "private" {
  subnet_id                 = azurerm_subnet.private.id
  network_security_group_id = azurerm_network_security_group.private.id
}

resource "azurerm_application_security_group" "dev" {
  name                = "${var.environment_name}-dev-asg"
  location            = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_application_security_group" "public" {
  name                = "${var.environment_name}-public-asg"
  location            = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_application_security_group" "private" {
  name                = "${var.environment_name}-private-asg"
  location            = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_subnet" "gateway" {
  name                 = "GatewaySubnet"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = [var.gateway_subnet_cidr]
}