
#new locals for lacp_interface_policy

locals {
  yaml_lacp_policy= yamldecode(file("${path.module}/lacp_policy_vars.yml"))
}



output "lacp_policy_details" {
  value = { for t in local.yaml_lacp_policy.lacp_policy : t.lacp_policy => t }
}


# resource "aci_tenant" "tenants" {
#   for_each = { for t in local.yaml__level_policy._level_policy : t._level_policy => t }

#   name        = each.value.tenant
#   description = each.value.description
# }


# # lldp policies
# resource "aci_fabric_if_pol" "llpols" {
#   for_each = { for t in local.yaml_link_level_policy.link_level_policy : t.link_level_policy => t }
#   #for_each      = var.intpols
#   name          = each.value.link_level_policy
#   description   = each.value.description
#   auto_neg      = each.value.autoneg
#   fec_mode      = each.value.fec
#   link_debounce = each.value.linkdebounce
#   speed         = each.value.speed
# }



# # LACP policies
# resource "aci_lldp_interface_policy" "lldp_pols" {
#   for_each = { for t in local.yaml_lldp_policy.lldp_policy : t.lldp_policy => t }
#   #for_each    = var.lldp
#   description = each.value.description
#   name        = each.value.lldp_policy
#   admin_rx_st = each.value.receive
#   admin_tx_st = each.value.transmit
# }

# LACP policies
resource "aci_lacp_policy" "lacp_pols" {
  for_each = { for t in local.yaml_lacp_policy.lacp_policy : t.lacp_policy => t }
  name      = each.value.lacp_policy
  max_links = each.value.max_links
  min_links = each.value.min_links
  mode      = each.value.mode
}
