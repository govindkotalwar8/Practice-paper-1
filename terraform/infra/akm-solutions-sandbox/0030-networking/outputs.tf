output "vnet_id" {
  value = module.networking.vnet_id
}

output "public_subnet_id" {
  value = module.networking.public_subnet_id
}

output "private_subnet_id" {
  value = module.networking.private_subnet_id
}

output "gateway_subnet_id" {
  value = module.networking.gateway_subnet_id
}