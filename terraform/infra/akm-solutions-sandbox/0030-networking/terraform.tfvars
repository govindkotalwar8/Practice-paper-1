location            = "northeurope"
resource_group_name = "experimental-govind-kotalwar"

environment_name    = "test"

vnet_cidr           = ["10.0.0.0/16"]
public_subnet_cidr  = ["10.0.1.0/24"]
private_subnet_cidr = ["10.0.2.0/24"]

developer_ip = ["122.183.33.123/32"]
gateway_subnet_cidr = "10.0.255.0/27"