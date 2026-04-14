output "vpn_gateway_id" {
  value = azurerm_virtual_network_gateway.vpn_gateway.id
}

output "vpn_public_ip" {
  value = azurerm_public_ip.vpn_pip.ip_address
}