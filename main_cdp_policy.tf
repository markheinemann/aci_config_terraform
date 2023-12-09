
#new locals for cdp_interface_policy

locals {
  yaml_cdp_policy= yamldecode(file("${path.module}/cdp_policy_vars.yml"))
}



output "cdp_policy_details" {
  value = { for t in local.yaml_cdp_policy.cdp_policy : t.cdp_policy => t }
}


# CDP policies
resource "aci_cdp_interface_policy" "cdp_pols" {
  for_each = { for t in local.yaml_cdp_policy.cdp_policy : t.cdp_policy => t }
  description = each.value.description
  name        = each.value.cdp_policy
  admin_st    = each.value.admin_state
}
