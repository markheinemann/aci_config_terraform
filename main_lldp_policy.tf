#new locals for lldp_interface_policy

locals {
  yaml_lldp_policy= yamldecode(file("${path.module}/lldp_policy_vars.yml"))
}



output "lldp_policy_details" {
  value = { for t in local.yaml_lldp_policy.lldp_policy : t.lldp_policy => t }
}


# LLDP policies
resource "aci_lldp_interface_policy" "lldp_pols" {
  for_each = { for t in local.yaml_lldp_policy.lldp_policy : t.lldp_policy => t }
  description = each.value.description
  name        = each.value.lldp_policy
  admin_tx_st     = each.value.transmit
  admin_rx_st    = each.value.receive
}