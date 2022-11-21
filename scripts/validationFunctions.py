#Imports
from bigrest.bigip import BIGIP
from bigrest.utils.utils import rest_format
from bigrest.utils.utils import token


import urllib.parse
import helper
import json



def getDeviceInfo(_device,_selfDevice):
# Gets relevant information from '/mgmt/tm/cm/device'
# that is useful for validation testing. 
    rest_details = _device.load(
        f"/mgmt/tm/cm/device"
    )

    columns = {
        "hostname":"hostname",
        "selfDevice":"selfDevice",
        "management IP":"managementIp",
        "version":"version",
        "build":"build",
        "edition":"edition",
        "failover state":"failoverState",
        "MAC Address":"baseMac"
    }
    
    if(_selfDevice =="self"):
        for item in rest_details:
            print(item.asdict()["selfDevice"])
            if(item.asdict()['selfDevice'] == "true"):
                rest_object = item
    elif(_selfDevice == "other"):
        rest_object = []
        for item in rest_details:
            if(item.asdict()['selfDevice'] == "false"):
                rest_object.append(item)
    else:
        rest_object = rest_details

    
    return helper.filter_restobject(rest_object,columns)


def getLicenseInfo(_device):
 # Gets information from /mgmt/tm/sys/license
 # formats it in an easier to read way
    rest_details = _device.show(
        f"/mgmt/tm/sys/license"
    )

    rest_dict = rest_details.asdict()

    license_info = {
        "base" : {
            "licenseStartDate":rest_dict["licenseStartDate"]["description"],
            "licenseEndDate":rest_dict["licenseEndDate"]["description"],
            "licensedOnDate":rest_dict["licensedOnDate"]["description"],
            "licensedVersion":rest_dict["licensedVersion"]["description"],
            "serviceCheckDate":rest_dict["serviceCheckDate"]["description"],
            "registrationKey":rest_dict["registrationKey"]["description"]
        },
        "time_limited_modules":[]
    }

    tl_modules = rest_dict["https://localhost/mgmt/tm/sys/license/0/time-limited-modules/stats"]["nestedStats"]["entries"]
    for i in tl_modules:
        components = i.split("/")
        decoded = urllib.parse.unquote(components[-2])
        module = {
            "name":decoded.replace("\"",""),
            "key":tl_modules[i]["nestedStats"]["entries"]["key"]["description"],
            "timeStart":tl_modules[i]["nestedStats"]["entries"]["timeStart"]["description"],
            "timeEnd":tl_modules[i]["nestedStats"]["entries"]["timeEnd"]["description"]
        }
        license_info["time_limited_modules"].append(module)
    return license_info





def getVirtualServerInfo(_device, detailed):
    # Return information about virutal server availability.

    # If detailed == true, then per virtual server information will be provided, else just
    # a high level summary.

    #TODO: Perhaps adding filter options...
    # and parameter validation??




    virtualServerInfo = {
        "summary" : {
            "total":0,
            "status_unknown":0,
            "status_available":0,
            "status_offline":0,
            "status_other":0,
            "state_enabled":0,
            "state_disabled":0
        },
        "detailed":[]
    }

    rest_details = _device.show(f"/mgmt/tm/ltm/virtual")

    # Loop through virtual servers to create summary of availability/status
    for i in rest_details:
        rest_dict = i.asdict() #Convert to a dict
        virtualServerInfo["summary"]["total"]+=1
        availability_status = rest_dict["status.availabilityState"]["description"]

        if ( availability_status == "unknown") :
            virtualServerInfo["summary"]["status_unknown"] += 1
        elif (availability_status == "available"):
            virtualServerInfo["summary"]["status_available"] += 1
        elif (availability_status == "offline"):
            virtualServerInfo["summary"]["status_offline"] += 1
        else:
            virtualServerInfo["summary"]["status_other"] += 1

        
        enabled_state = rest_dict["status.enabledState"]["description"]
        if( enabled_state == "enabled" ):
            virtualServerInfo["summary"]["state_enabled"] += 1
        elif ( enabled_state == "disabled" ):
            virtualServerInfo["summary"]["state_disabled"] += 1

        # If a detailed (per-vs) response is required, add that.
        # Currently only planning on returning status and state (i.e. available but disabled)
        if( detailed is True ):
            print(json.dumps(rest_dict))
            virtualServer = {
                "name":rest_dict["tmName"]["description"],
                "state":rest_dict["status.enabledState"]["description"],
                "availability":rest_dict["status.availabilityState"]["description"]
            }

            virtualServerInfo["detailed"].append(virtualServer)
            

    
        
    return virtualServerInfo

        


