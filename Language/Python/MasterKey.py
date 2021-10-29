import subprocess
import re

#Runs a cmd command that shows all profiles that the device has already connected with
#Example:
#User profiles
#-------------
#		All User Profile     : Switch
#		All User Profile     : Terrincha_6
#		All User Profile     : HUAWEI P20 lite
#		All User Profile     : eduroam
#		All User Profile     : NOS-AF90 2
#		All User Profile     : ESAPWINET
#		All User Profile     : BD
#		All User Profile     : NOS-AF90
#		All User Profile     : NOS_Wi-Fi_Hotspots
# 		All User Profile     : ShowRoom
#  		All User Profile     : Abimota-Wifi
#       All User Profile     : WAP02
#    	All User Profile     : wifi-clientes



command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

wifi_list = list()

if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = dict()
        #Runs the same code line but showing the info of one individualy
        #Profile Switch on interface Wi-Fi 3:
#=======================================================================

#Applied: All User Profile

#Profile information
#-------------------
#    Version                : 1
#    Type                   : Wireless LAN
#    Name                   : Switch
#    Control options        :
#        Connection mode    : Connect automatically
#        Network broadcast  : Connect only if this network is broadcasting
#        AutoSwitch         : Do not switch to other networks
#        MAC Randomization  : Disabled

#Connectivity settings
#---------------------
#    Number of SSIDs        : 1
#    SSID name              : "Switch"
#    Network type           : Infrastructure
#    Radio type             : [ Any Radio Type ]
#    Vendor extension          : Not present

#Security settings
#-----------------
#    Authentication         : WPA2-Personal
#    Cipher                 : CCMP
#    Authentication         : WPA2-Personal
#    Cipher                 : GCMP
#    Security key           : Present (In this case the Security Key is Present witch means that can "extract"/show it, 
#										if the security key was presented as Absent, means that the key will not appear
#										and it´s not available for the regular user)

#Cost settings
#-------------
#    Cost                   : Unrestricted
#    Congested              : No
#    Approaching Data Limit : No
#    Over Data Limit        : No
#    Roaming                : No
#    Cost Source            : Default

        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name

            #Runs the code line to show the info of a network profile individualy and clears the Security Key to show the password
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
            wifi_list.append(wifi_profile) 

for x in range(len(wifi_list)):
    print(wifi_list[x]) 