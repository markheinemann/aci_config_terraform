import csv
import yaml
from collections import defaultdict
import subprocess
import os
import shutil
import openpyxl
import pprint



##############################################
#          PROCESS tenants            #
##############################################

xlsx_file_path = "Book2.xlsx"
worksheet_name = "TENANT"

output_yaml_file_path_leaf = "tenant_vars.yml"

data_tenant = defaultdict(list)

# Open the Excel file
workbook = openpyxl.load_workbook(xlsx_file_path)

# Select the worksheet by name
worksheet = workbook[worksheet_name]

# Iterate through rows in the worksheet
for row in worksheet.iter_rows(min_row=2, values_only=True):
    type = row[0]  # Assuming "type" is in the first column
    print(type)

    if type == "tenant":
        print("match tenant")
        data_tenant[type].append({
            "tenant_name": row[1],  # Assuming "tenant_name" is in the second column
            "tenant_description": row[2]  # Assuming "tenant_description" is in the third column
        })


with open(output_yaml_file_path_leaf, 'w') as yaml_file:
    for function, items in data_tenant.items():
        yaml_file.write("{}:\n".format(function))
        for item in items:
#            print(item)
            yaml_file.write("- tenant: {}\n".format(item["tenant_name"]))



            yaml_file.write("  description: {}\n".format(item["tenant_description"]))

            yaml_file.write("\n")




# Close the Excel file
#workbook.close()

pprint.pprint(data_tenant)

# #sys.exit()

##############################################
#          PROCESS vrf           #
##############################################

xlsx_file_path = "Book2.xlsx"
worksheet_name = "VRF"

output_yaml_file_path_leaf = "vrf_vars.yml"

data_vrf = defaultdict(list)

# Open the Excel file
workbook = openpyxl.load_workbook(xlsx_file_path)

# Select the worksheet by name
worksheet = workbook[worksheet_name]

# Iterate through rows in the worksheet
for row in worksheet.iter_rows(min_row=2, values_only=True):
    type = row[0]  # Assuming "type" is in the first column
    print(type)

    if type == "vrf":
        
        data_vrf[type].append({
            "vrf_name": row[1],  
            "vrf_tenant": data_tenant["tenant"][0]["tenant_name"]
        })


with open(output_yaml_file_path_leaf, 'w') as yaml_file:
    for function, items in data_vrf.items():
        yaml_file.write("{}:\n".format(function))
        for item in items:
#            print(item)
            yaml_file.write("- vrf: {}\n".format(item["vrf_name"]))
            yaml_file.write("  vrf_tenant: {}\n".format(item["vrf_tenant"]))
            yaml_file.write("\n")




# Close the Excel file
#workbook.close()

pprint.pprint(data_vrf)



##############################################
#          PROCESS bd            #
##############################################

xlsx_file_path = "Book2.xlsx"
worksheet_name = "BD"

output_yaml_file_path_leaf = "bd_vars.yml"

data_bd = defaultdict(list)

# Open the Excel file
#workbook = openpyxl.load_workbook(xlsx_file_path)
worksheet = workbook[worksheet_name]

for row in worksheet.iter_rows(min_row=2, values_only=True):
    type = row[0]  # Assuming "type" is in the first column
    print(type)

    if type == "bd":
        #print("match")
        data_bd[type].append({
            "bd_tenant_name": data_tenant["tenant"][0]["tenant_name"],
            "bd_name": row[1],
            "bd_description": row[2],
            "bd_vrf": data_vrf['vrf'][0]['vrf_name']
        })


with open(output_yaml_file_path_leaf, 'w') as yaml_file:
    for function, items in data_bd.items():
        yaml_file.write("{}:\n".format(function))
        for item in items:
#            print(item)
            yaml_file.write("- bd: {}\n".format(item["bd_name"]))
            yaml_file.write("  bd_tenant_name: {}\n".format(item["bd_tenant_name"]))
            yaml_file.write("  bd_description: {}\n".format(item["bd_description"]))
            yaml_file.write("  bd_vrf: {}\n".format(item["bd_vrf"]))
            yaml_file.write("\n")

pprint.pprint(data_bd)






##############################################
#          PROCESS subnet          #
##############################################
xlsx_file_path = "Book2.xlsx"
worksheet_name = "SUBNET"

output_yaml_file_path_leaf = "subnet_vars.yml"

data_subnet = defaultdict(list)

# Open the Excel file
#workbook = openpyxl.load_workbook(xlsx_file_path)
worksheet = workbook[worksheet_name]

for row in worksheet.iter_rows(min_row=2, values_only=True):
    type = row[0]  # Assuming "type" is in the first column
    print(type)

    if type == "subnet":
        data_subnet[type].append({
            "subnet_name": row[1],
            "subnet_tn_name": data_tenant["tenant"][0]["tenant_name"],
            "subnet_bd": row[2],
            "subnet_scope": row[3],
            "subnet_description": row[4]
        })

with open(output_yaml_file_path_leaf, 'w') as yaml_file:
    for function, items in data_subnet.items():
        yaml_file.write("{}:\n".format(function))
        for item in items:
#            print(item)
            yaml_file.write("- subnet: {}\n".format(item["subnet_name"]))
            yaml_file.write("  subnet_tn_name: {}\n".format(item["subnet_tn_name"]))
            yaml_file.write("  subnet_bd: {}\n".format(item["subnet_bd"]))
            yaml_file.write("  subnet_scope: {}\n".format(item["subnet_scope"]))
            yaml_file.write("  subnet_description: {}\n".format(item["subnet_description"]))
            yaml_file.write("\n")


#
pprint.pprint(data_subnet)













###

##############################################
#          PROCESS application_profile        #
##############################################

xlsx_file_path = "Book2.xlsx"
worksheet_name = "APP_PROFILE"

output_yaml_file_path_leaf = "app_profile_vars.yml"

data_app_profile = defaultdict(list)

# Open the Excel file
#workbook = openpyxl.load_workbook(xlsx_file_path)
worksheet = workbook[worksheet_name]

for row in worksheet.iter_rows(min_row=2, values_only=True):
    type = row[0]  # Assuming "type" is in the first column
    print(type)


    if type == "app_profile":
            data_app_profile[type].append({
                "app_profile_name": row[1],
                "app_profile_tenant": data_tenant["tenant"][0]["tenant_name"]
            })

with open(output_yaml_file_path_leaf, 'w') as yaml_file:
    for function, items in data_app_profile.items():
        yaml_file.write("{}:\n".format(function))
        for item in items:
#            print(item)
            yaml_file.write("- app_profile: {}\n".format(item["app_profile_name"]))
            yaml_file.write("  app_profile_tenant: {}\n".format(item["app_profile_tenant"]))


            yaml_file.write("\n")



pprint.pprint(data_app_profile)






##############################################
#          PROCESS epg       #
##############################################

xlsx_file_path = "Book2.xlsx"
worksheet_name = "EPG"

output_yaml_file_path_leaf = "epg_vars.yml"

data_epg = defaultdict(list)

# Open the Excel file
#workbook = openpyxl.load_workbook(xlsx_file_path)
worksheet = workbook[worksheet_name]

for row in worksheet.iter_rows(min_row=2, values_only=True):
    type = row[0]  # Assuming "type" is in the first column
    print(type)



    if type == "epg":
        data_epg[type].append({
            "epg_name": row[1],
            "epg_tenant": data_tenant["tenant"][0]["tenant_name"],
            "epg_map_to_bd": row[2],
            "epg_map_to_app_profile": row[3]
        })

with open(output_yaml_file_path_leaf, 'w') as yaml_file:
    for function, items in data_epg.items():
        yaml_file.write("{}:\n".format(function))
        for item in items:
#            print(item)
            yaml_file.write("- epg: {}\n".format(item["epg_name"]))
            yaml_file.write("  epg_tenant: {}\n".format(item["epg_tenant"]))
            yaml_file.write("  epg_map_to_bd: {}\n".format(item["epg_map_to_bd"]))
            yaml_file.write("  epg_map_to_app_profile: {}\n".format(item["epg_map_to_app_profile"]))

            
            yaml_file.write("\n")

pprint.pprint(data_epg)


# Close the Excel file
workbook.close()


#sys.exit()


            # vlan_segments = item["vlan_segments"]
            # for i, segment in enumerate(vlan_segments):
            #     if "," in segment:
            #         vlan, vn_segment = segment.split(",", 1)
            #         vlan_key = "Vlan{}".format(i+1)
            #         segment_key = "vn segment{}".format(i+1)
            #         yaml_file.write("  {}: {}\n".format(vlan_key, vlan.strip()))
            #         yaml_file.write("  {}: {}\n".format(segment_key, vn_segment.strip()))


            # interface_to_spine = item["interface_to_spine"]
            # for i, description in enumerate(interface_to_spine):
            #     if "," in description:
            #         interface, desc = description.split(",", 1)
            #         interface_key = "Ethernet{}".format(i+1)
            #         desc_key = "description{}".format(i+1)
            #         yaml_file.write("  {}: {}\n".format(interface_key, interface.strip()))
            #         yaml_file.write("  {}: {}\n".format(desc_key, desc.strip()))


            # yaml_file.write("  vrf: {}\n".format(item["vrf"]))

            # yaml_file.write("  vlan:\n")
            # for vlan in item["vlan"]:
            #     yaml_file.write("    - {}\n".format(vlan))

            # yaml_file.write("  l3vni: {}\n".format(item["l3vni"]))

            # yaml_file.write("  l3vni_svi: {}\n".format(item["l3vni_svi"]))

            # vlan_anycast_gw = item["vlan_anycast_gw"]
            # for i, gateway in enumerate(vlan_anycast_gw):
            #     if "," in gateway:
            #         vlan, gw = gateway.split(",", 1)
            #         vlan_key = "gw_vlan{}".format(i+1)
            #         gw_key = "vlan_anycast_gateway{}".format(i+1)
            #         yaml_file.write("  {}: {}\n".format(vlan_key, vlan.strip()))
            #         yaml_file.write("  {}: {}\n".format(gw_key, gw.strip()))

            # yaml_file.write("  anycast_gateway_mac: {}\n".format(item["anycast_gateway_mac"]))

            # yaml_file.write("  ospf_process: {}\n".format(item["ospf_process"]))

            # yaml_file.write("  nve_multicast_grp: {}\n".format(item["nve_multicast_grp"]))

            # yaml_file.write("  pim_rp_address: {}\n".format(item["pim_rp_address"]))

            # yaml_file.write("  pim_grp_list: {}\n".format(item["pim_grp_list"]))

            # yaml_file.write("  pim_ssm_range: {}\n".format(item["pim_ssm_range"]))

            # yaml_file.write("  local_bgp_as: {}\n".format(item["local_bgp_as"]))

            # yaml_file.write("  remote_bgp_as: {}\n".format(item["remote_bgp_as"]))

            # yaml_file.write("  bgp_neighbor:\n")
            # for bgp_neighbor in item["bgp_neighbor"]:
            #     yaml_file.write("    - {}\n".format(bgp_neighbor))

            # yaml_file.write("  advertised_network:\n")
            # for advertised_network in item["advertised_network"]:
            #     yaml_file.write("    - {}\n".format(advertised_network))


            
            #yaml_file.write("\n")
        #print(f"YAML file generated at: {output_yaml_file_path_leaf}")


#         # move the extraced vars to roles/leaf/vars

#         # Define the source file path for LEAF
#         source_file = 'leaf_evpn_vars.yml'

#         # Define the destination folder path
#         destination_folder = 'roles/leaf/vars'

#         # Define the new file name
#         new_file_name = 'main.yml'

#         # Create the full path for the destination file
#         destination_file = os.path.join(destination_folder, new_file_name)

#         # Move the file to the destination folder
#         shutil.move(source_file, destination_file)

#         # Output a success message
#         print(f"The file '{source_file}' has been moved to '{destination_file}' and renamed to '{new_file_name}'.")




# # NOW REPEAT EXTRACTION FOR SPINE VARS #
# #
# #
# #
# #
# #

# csv_file_path = "file3.csv"
# output_yaml_file_path_spine = "spine_evpn_vars.yml"

# data = defaultdict(list)  # Use defaultdict to group data by function

# with open(csv_file_path, 'r') as csv_file:
#     reader = csv.DictReader(csv_file)
#     for row in reader:
#         function = row["function"]
#         print(function)

# ##############################################
# #          PROCESS SPINES in CVS              #
# ##############################################


#         if function == "spine":
#             data[function].append({
#                 "hostname": row["hostname"],
#                 "features": row["feature"].split(","),
#                 "loopback": row["loopback0"],# + "/32",
#                 "loopback1": row["loopback1"],# + "/32",
#                 #"vlan_segments": row["Vlan <> vn segment"].split("\n"),
#                 "interface_to_leaf": row["downlink_to_leaf"].split("\n"),
#                 #"vrf": row["vrf"],
# 	            #"vlan": row["vlan"].split(","),
#                 #"l3vni": row["L3vni"],
#                 #"l3vni_svi": row["L3vni_svi"],
#                 #"vlan_anycast_gw": row["vlan <> anycast_gw"].split("\n"),
#                 #"anycast_gateway_mac": row["anycast_gateway_mac"],
#                 "ospf_process": row["ospf_process"],
#                 #"nve_multicast_grp": row["nve_multicast_grp"],
#                 "pim_rp_address": row["pim_rp_address"],
#                 "pim_grp_list": row["pim_grp_list"],
#                 "pim_ssm_range": row["pim_ssm_range"],
#                 "spine_rp_address": row["spine_rp_address"].split(","),
#                 "local_bgp_as": row["local_bgp_as"],
#                 "remote_bgp_as": row["remote_bgp_as"],
#                 "bgp_neighbor": row["bgp_neighbor"].split(","),
#                 #"advertised_network": row["advertised_network"].split(",")
#             })

# with open(output_yaml_file_path_spine, 'w') as yaml_file:
#     for function, items in data.items():
#         yaml_file.write("{}:\n".format(function))
#         for item in items:
# #            print(item)
#             yaml_file.write("- hostname: {}\n".format(item["hostname"]))

#             yaml_file.write("  features:\n")
#             for feature in item["features"]:
#                 yaml_file.write("    - {}\n".format(feature))

#             yaml_file.write("  loopback0: {}\n".format(item["loopback"]))

#             yaml_file.write("  loopback1: {}\n".format(item["loopback1"]))

# #            vlan_segments = item["vlan_segments"]
# #            for i, segment in enumerate(vlan_segments):
# #                if "," in segment:
# #                    vlan, vn_segment = segment.split(",", 1)
# #                    vlan_key = "Vlan{}".format(i+1)
# #                    segment_key = "vn segment{}".format(i+1)
# #                    yaml_file.write("  {}: {}\n".format(vlan_key, vlan.strip()))
# #                    yaml_file.write("  {}: {}\n".format(segment_key, vn_segment.strip()))


#             interface_to_leaf = item["interface_to_leaf"]
#             for i, description in enumerate(interface_to_leaf):
#                 if "," in description:
#                     interface, desc = description.split(",", 1)
#                     interface_key = "Ethernet{}".format(i+1)
#                     desc_key = "description{}".format(i+1)
#                     yaml_file.write("  {}: {}\n".format(interface_key, interface.strip()))
#                     yaml_file.write("  {}: {}\n".format(desc_key, desc.strip()))


# #            yaml_file.write("  vrf: {}\n".format(item["vrf"]))

# #            yaml_file.write("  vlan:\n")
# #            for vlan in item["vlan"]:
# #                yaml_file.write("    - {}\n".format(vlan))

# #            yaml_file.write("  l3vni: {}\n".format(item["l3vni"]))

# #            yaml_file.write("  l3vni_svi: {}\n".format(item["l3vni_#svi"]))

# #            vlan_anycast_gw = item["vlan_anycast_gw"]
# #            for i, gateway in enumerate(vlan_anycast_gw):
# #                if "," in gateway:
# #                    vlan, gw = gateway.split(",", 1)
# #                    vlan_key = "gw_vlan{}".format(i+1)
# #                    gw_key = "vlan_anycast_gateway{}".format(i+1)
# #                    yaml_file.write("  {}: {}\n".format(vlan_key, vlan.strip()))
# #                    yaml_file.write("  {}: {}\n".format(gw_key, gw.strip()))

# #            yaml_file.write("  anycast_gateway_mac: {}\n".format(item["anycast_gateway_mac"]))

#             yaml_file.write("  ospf_process: {}\n".format(item["ospf_process"]))

# #            yaml_file.write("  nve_multicast_grp: {}\n".format(item["nve_multicast_grp"]))

#             yaml_file.write("  pim_rp_address: {}\n".format(item["pim_rp_address"]))

#             yaml_file.write("  pim_grp_list: {}\n".format(item["pim_grp_list"]))

#             yaml_file.write("  pim_ssm_range: {}\n".format(item["pim_ssm_range"]))

#             yaml_file.write("  spine_rp_address:\n")
#             for spine_rp_address in item["spine_rp_address"]:
#                 yaml_file.write("    - {}\n".format(spine_rp_address))

#             yaml_file.write("  local_bgp_as: {}\n".format(item["local_bgp_as"]))

#             yaml_file.write("  remote_bgp_as: {}\n".format(item["remote_bgp_as"]))

#             yaml_file.write("  bgp_neighbor:\n")
#             for bgp_neighbor in item["bgp_neighbor"]:
#                 yaml_file.write("    - {}\n".format(bgp_neighbor))

# #            yaml_file.write("  advertised_network:\n")
# #            for advertised_network in item["advertised_network"]:
# #                yaml_file.write("    - {}\n".format(advertised_network))


            
#             yaml_file.write("\n")
#         print(f"YAML file generated at: {output_yaml_file_path_spine}")


#         # move the extraced vars to roles/spine/vars

#         # Define the source file path for LEAF
#         source_file = 'spine_evpn_vars.yml'

#         # Define the destination folder path
#         destination_folder = 'roles/spine/vars'

#         # Define the new file name
#         new_file_name = 'main.yml'

#         # Create the full path for the destination file
#         destination_file = os.path.join(destination_folder, new_file_name)

#         # Move the file to the destination folder
#         shutil.move(source_file, destination_file)

# # Output a success message
# print(f"The file '{source_file}' has been moved to '{destination_file}' and renamed to '{new_file_name}'.")

# print(" PYTHON EXTRACTION COMPLETE- VARS EXTRACTED FROM CSV SUCCESSFULLY")
# print("NOW RUNNING ANSIBLE PLAYBOOK TO WRITE CONFIG FILES")











# #run ansible script to generate configs

# ansible_command = ['ansible-playbook', 'site.yml']
# print(ansible_command)

# subprocess.run(ansible_command, check=True)









