# -------------------------------
# SSH: Dev → Public VM
# -------------------------------
resource "azurerm_network_security_rule" "ssh" {
  name                        = "ssh"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"

  source_port_range           = "*"
  destination_port_range      = "22"

  source_application_security_group_ids = [
    azurerm_application_security_group.dev.id
  ]

  destination_application_security_group_ids = [
    azurerm_application_security_group.public.id
  ]

  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.public.name
}

# -------------------------------
# Public TCP: Dev → Public VM
# -------------------------------
resource "azurerm_network_security_rule" "public_tcp" {
  name                        = "public-tcp"
  priority                    = 110
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"

  source_port_range           = "*"
  destination_port_ranges     = local.public_inbound_tcp_ports

  source_application_security_group_ids = [
    azurerm_application_security_group.dev.id
  ]

  destination_application_security_group_ids = [
    azurerm_application_security_group.public.id
  ]

  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.public.name
}

# -------------------------------
# Postgres: Public VM → Private DB
# -------------------------------
resource "azurerm_network_security_rule" "postgres" {
  name                        = "postgres"
  priority                    = 120
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"

  source_port_range           = "*"
  destination_port_range      = "5432"

  source_application_security_group_ids = [
    azurerm_application_security_group.public.id
  ]

  destination_application_security_group_ids = [
    azurerm_application_security_group.private.id
  ]

  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.private.name
}