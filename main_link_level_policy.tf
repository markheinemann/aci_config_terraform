# provider "aci" {
#   # cisco-aci user name
#   username = "admin"
#   # cisco-aci password
#   password = "!v3G@!4@Y"
#   # cisco-aci url
#   url      =  "https://sandboxapicdc.cisco.com"
#   insecure = true
# }



#new locals for link_level_policy

locals {
  yaml_link_level_policy= yamldecode(file("${path.module}/link_level_policy_vars.yml"))
}



output "link_level_policy_details" {
  value = { for t in local.yaml_link_level_policy.link_level_policy : t.link_level_policy => t }
}


# resource "aci_tenant" "tenants" {
#   for_each = { for t in local.yaml__level_policy._level_policy : t._level_policy => t }

#   name        = each.value.tenant
#   description = each.value.description
# }


# Link level policies
resource "aci_fabric_if_pol" "llpols" {
  for_each = { for t in local.yaml_link_level_policy.link_level_policy : t.link_level_policy => t }
  #for_each      = var.intpols
  name          = each.value.link_level_policy
  description   = each.value.description
  auto_neg      = each.value.autoneg
  fec_mode      = each.value.fec
  link_debounce = each.value.linkdebounce
  speed         = each.value.speed
}