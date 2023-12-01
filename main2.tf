provider "aci" {
  # cisco-aci user name
  username = "admin"
  # cisco-aci password
  password = "!v3G@!4@Y"
  # cisco-aci url
  url      =  "https://sandboxapicdc.cisco.com"
  insecure = true
}


#new locals for tenants

locals {
  yaml_tenants= yamldecode(file("${path.module}/tenant_vars.yml"))
}



output "tenant_details" {
  value = { for t in local.yaml_tenants.tenant : t.tenant => t }
}


resource "aci_tenant" "tenants" {
  for_each = { for t in local.yaml_tenants.tenant : t.tenant => t }

  name        = each.value.tenant
  description = each.value.description
}













#new locals for bd


locals {
  yaml_bd= yamldecode(file("${path.module}/bd_vars.yml"))
}

output "yaml_bd_content" {
  value = local.yaml_bd
}

output "bd_details" {
  value = { for t in local.yaml_bd.bd : t.bd => t }
}

resource "aci_bridge_domain" "bridge_domains" {
  for_each = { for t in local.yaml_bd.bd : t.bd => t }
  tenant_dn   = "uni/tn-${each.value.bd_tenant_name}"
  name        = each.value.bd
  description = each.value.bd_description
  relation_fv_rs_ctx = "uni/tn-${each.value.bd_tenant_name}/ctx-${each.value.bd_vrf}"
  #relation_fv_rs_ctx = "marks_vrf"




  depends_on = [
    aci_tenant.tenants,
    aci_vrf.vrfs,
  ]
}

output "bridge_domain_dns" {
  value = [for bd_key, bd_value in aci_bridge_domain.bridge_domains : aci_bridge_domain.bridge_domains[bd_key].relation_fv_rs_ctx]
}




#new locals for aci subnets


locals {
  yaml_subnet= yamldecode(file("${path.module}/subnet_vars.yml"))
}

output "subnet_details" {
  value = { for t in local.yaml_subnet.subnet : t.subnet => t }
}

resource "aci_subnet" "aci_subnets" {
  for_each = { for t in local.yaml_subnet.subnet : t.subnet => t }
  parent_dn    = "uni/tn-${each.value.subnet_tn_name}/BD-${each.value.subnet_bd}"
  ip        = each.value.subnet
  description = each.value.subnet_description
  scope = [each.value.subnet_scope]

  depends_on = [
    aci_tenant.tenants,
    aci_bridge_domain.bridge_domains,
  ]
}



#new locals for epg


locals {
  yaml_epg= yamldecode(file("${path.module}/epg_vars.yml"))
}

output "epg_details" {
  value = { for t in local.yaml_epg.epg : t.epg => t }
}

resource "aci_application_epg" "epgs" {
  for_each = { for t in local.yaml_epg.epg: t.epg => t }
  name = each.value.epg
  application_profile_dn = "uni/tn-${each.value.epg_tenant}/ap-${each.value.epg_map_to_app_profile}"
  relation_fv_rs_bd = "uni/tn-${each.value.epg_tenant}/BD-${each.value.epg_map_to_bd}"

  depends_on = [
    aci_tenant.tenants,
    aci_application_profile.app_profiles,
    aci_bridge_domain.bridge_domains,
  ]
}


# new locals for application_profile


locals {
  yaml_app_profile= yamldecode(file("${path.module}/app_profile_vars.yml"))
}

output "app_profile_details" {
  value = { for t in local.yaml_app_profile.app_profile : t.app_profile => t }
}

resource "aci_application_profile" "app_profiles" {
  for_each = { for t in local.yaml_app_profile.app_profile : t.app_profile => t }
  tenant_dn    = "uni/tn-${each.value.app_profile_tenant}"
  name        = each.value.app_profile

  depends_on = [
    aci_tenant.tenants,
  ]
}

#new locals for vrf


locals {
  yaml_vrf= yamldecode(file("${path.module}/vrf_vars.yml"))
}

output "vrf_details" {
  value = { for t in local.yaml_vrf.vrf : t.vrf => t }
}

resource "aci_vrf" "vrfs" {
  for_each = { for t in local.yaml_vrf.vrf: t.vrf => t }
  name = each.value.vrf
  tenant_dn = "uni/tn-${each.value.vrf_tenant}"
  #aci_tenant_fv_ctx_att = 
  

  depends_on = [
    aci_tenant.tenants,
  ]
}


#new locals for Vlan_Pool


locals {
  yaml_vlan_pool= yamldecode(file("${path.module}/vlan_pool_vars.yml"))
}

output "vlan_pool_details" {
  value = { for t in local.yaml_vlan_pool.vlan_pool : t.vlan_pool => t }
}

# creating vlan pool
resource "aci_vlan_pool" "vlan_pool" {
  for_each = { for t in local.yaml_vlan_pool.vlan_pool: t.vlan_pool => t }
  name  = each.value.vlan_pool
  description = "From Terraform"
  alloc_mode  = "static"
}

#create range
resource "aci_ranges" "range" {
  for_each = { for t in local.yaml_vlan_pool.vlan_pool: t.vlan_pool => t }
  #vlan_pool_dn  = "uni/infra/vlanns-[mark_pool]-static"
  vlan_pool_dn  = "uni/infra/vlanns-${each.value.vlan_pool}-${each.value.allocation_mode}"
  description   = "From Terraform"
  from          = each.value.range_from
  to            = each.value.range_to
  alloc_mode    = each.value.allocation_mode
  #role          = "external"


  depends_on = [
  aci_vlan_pool.vlan_pool
]
}

#new locals for Physical_Domain


locals {
  yaml_physical_domain= yamldecode(file("${path.module}/physical_domain_vars.yml"))
}

output "physical_domain_details" {
  value = { for t in local.yaml_physical_domain.physical_domain : t.physical_domain => t }
}

# creating physical_domain
resource "aci_physical_domain" "phys_domain" {
  for_each = { for t in local.yaml_physical_domain.physical_domain: t.physical_domain => t }
  name  = each.value.physical_domain
  #description = "From Terraform"
}
