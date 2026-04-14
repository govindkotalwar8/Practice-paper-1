output "vnet_id" {
  value = azurerm_virtual_network.this.id
}

output "public_subnet_id" {
  value = azurerm_subnet.public.id
}

output "private_subnet_id" {
  value = azurerm_subnet.private.id
}

output "public_nsg_id" {
  value = azurerm_network_security_group.public.id
}

output "private_nsg_id" {
  value = azurerm_network_security_group.private.id
}

output "nat_gateway_id" {
  value = azurerm_nat_gateway.this.id
}

output "nat_public_ip" {
  value = azurerm_public_ip.nat.ip_address
}

output "dev_asg_id" {
  value = azurerm_application_security_group.dev.id
}

output "gateway_subnet_id" {
  value = azurerm_subnet.gateway.id
}