#-------------------------------------------------------------------------------
# Updated:     2017-04-22
#
# Name:        get_sp_attributes_json.py
#
# Purpose:     Get pertinent attributes for a party_contact service provider
#              record and related records for data grids.
#
# Author:      Jeff Reinhart
#
# Created:     2017-04-22
#-------------------------------------------------------------------------------

import module_pfmm_get, module_pfmm_helpers
import json, cgi, datetime, time

def getSpAttributesJSON(spGid):
    # Dictionary to pass to JSON output
    attrDict = dict()

    # Get party_contact.serviceprovider
    pcSpObj = module_pfmm_get.cls_party_contact(spGid)

    if pcSpObj.globalIdExists:
        # Build list for html for record attributes
        attrDict["html"] = [
            {
                "type": "hidden",
                "name": "party_contacts.globalid.serviceprovider",
                "value": pcSpObj.globalid
            },
            {
                "caption": "Service Provider First Name",
                "type": "text",
                "name": "party_contacts.person_first_name.serviceprovider",
                "value": pcSpObj.person_first_name
            },
            {
                "caption": "Service Provider Last Name",
                "type": "text",
                "name": "party_contacts.person_last_name.serviceprovider",
                "value": pcSpObj.person_last_name
            },
            {
                "caption": "Service Provider Business Name",
                "type": "text",
                "name": "party_contacts.business_name.serviceprovider",
                "value": pcSpObj.business_name
            },
            {
                "caption": "Service Provider Business Type",
                "type": "text",
                "name": "party_contacts.business_type.serviceprovider",
                "value": pcSpObj.business_type
            },
            {
                "caption": "Service Provider Street Address",
                "type": "text",
                "name": "party_contacts.address_line_1.serviceprovider",
                "value": pcSpObj.address_line_1
            },
            {
                "caption": "Service Provider City",
                "type": "text",
                "name": "party_contacts.city.serviceprovider",
                "value": pcSpObj.city
            },
            {
                "caption": "Service Provider State",
                "type": "text",
                "name": "party_contacts.state_provice_short_name_code.serviceprovider",
                "value": pcSpObj.state_provice_short_name_code
            },
            {
                "caption": "Service Provider Zip",
                "type": "text",
                "name": "party_contacts.postal_code.serviceprovider",
                "value": pcSpObj.postal_code
            },
            {
                "caption": "Service Provider Do Not Mail",
                "type": "text",
                "name": "party_contacts.do_not_mail.serviceprovider",
                "value": pcSpObj.do_not_mail
            },
            {
                "caption": "Service Provider Phone 1",
                "type": "text",
                "name": "party_contacts.phone_line_1.serviceprovider",
                "value": pcSpObj.phone_line_1
            }
        ]

        # Get child tables
        pcSpChildTables = module_pfmm_get.relatedRecordGlobalIds('party_contacts', spGid)

        # Get contact_events
        attrDict["ceDgv"] = []
        contactEventGidList = pcSpChildTables['contact_events.party_contact_2_guid']
        for contactEventGid in contactEventGidList:
            # start temporary dict
            tempCeDict = dict()
            # get object
            contactEventObj = module_pfmm_get.cls_contact_event(contactEventGid)
            # add values to temp dict
            tempCeDict["contact_events.globalid"] = contactEventGid
            tempCeDict["contact_events.contact_date"] = module_pfmm_helpers.dateToYYYYMMDD(contactEventObj.contact_date)
            tempCeDict["contact_events.subject"] = contactEventObj.subject
            tempCeDict["contact_events.contact_event_type"] = contactEventObj.contact_event_type
            tempCeDict["contact_events.summary"] = contactEventObj.summary
            tempCeDict["contact_events.notes"] = contactEventObj.notes
            # get Land Contact party contact and add
            pcLoObj = module_pfmm_get.cls_party_contact(contactEventObj.party_contact_1_guid)
            tempCeDict["land_contact"] = module_pfmm_helpers.buildName(
                    pcLoObj.person_first_name,
                    pcLoObj.person_middle_name,
                    pcLoObj.person_last_name,
                    pcLoObj.person_name_prefix,
                    pcLoObj.person_name_suffix,
                    pcLoObj.spouse_name,
                    pcLoObj.business_name)
            # get Partner Forester party contact and add
            pcPfObj = module_pfmm_get.cls_party_contact(contactEventObj.party_contact_3_guid)
            tempCeDict["partner_forester"] = "{0} {1}".format(
                pcPfObj.person_first_name,
                pcPfObj.person_last_name)
            attrDict["ceDgv"].append(tempCeDict)

        # Get stewardship plan info for plans written
        attrDict["mpPwDgv"] = []
        mpPwGidList = pcSpChildTables['management_plans.party_contact_guid']
        for mpPwGid in mpPwGidList:
            mpPwObj = module_pfmm_get.cls_management_plan(mpPwGid)
            # match definition query for service
            if mpPwObj.plan_type == 'Stewardship' and \
               (mpPwObj.status == 'Complete' or mpPwObj.status == 'Revised'):
                # Get related ownership_block object and child tables
                obObj = module_pfmm_get.cls_ownership_block(mpPwObj.ownership_block_guid)
                obChildTbls = module_pfmm_get.relatedRecordGlobalIds('ownership_blocks', obObj.globalid)

                # Get ownership parcels
                opGids = obChildTbls['ownership_parcels']

                # Get party_cont_own_prcl, counties, and parcel PINs
                pcopGids = []
                for opGid in opGids:
                    opObj = module_pfmm_get.cls_ownership_parcel(opGid)
                    # party_cont_own_prcl
                    opChildTbls = module_pfmm_get.relatedRecordGlobalIds('ownership_parcels', opObj.globalid)
                    pcopGids += opChildTbls['party_cont_own_prcl']

                # Get party_contact.landcontact
                pcLoGid = module_pfmm_get.lastPcopPcGid(pcopGids)
                pcLoObj = module_pfmm_get.cls_party_contact(pcLoGid)

                # start temporary dict
                tempMpDict = dict()
                # management plan attributes
                tempMpDict["management_plans.globalid"] = mpPwGid
                tempMpDict["management_plans.plan_date"] = module_pfmm_helpers.dateToYYYYMMDD(mpPwObj.plan_date)
                tempMpDict["management_plans.acres_plan"] = mpPwObj.acres_plan
                # get land contact
                tempMpDict["land_contact"] = module_pfmm_helpers.buildName(
                    pcLoObj.person_first_name,
                    pcLoObj.person_middle_name,
                    pcLoObj.person_last_name,
                    pcLoObj.person_name_prefix,
                    pcLoObj.person_name_suffix,
                    pcLoObj.spouse_name,
                    pcLoObj.business_name)
                # get plan writer
                pcPwObj = module_pfmm_get.cls_party_contact(mpPwObj.party_contact_guid)
                tempMpDict["plan_writer"] = "{0} {1} - {2}".format(
                    pcPwObj.person_first_name,
                    pcPwObj.person_last_name,
                    pcPwObj.business_name)
                # trs from owner block
                tempMpDict["pls_section"] = "T{0}N-R{1}{2}-S{3}".format(
                    obObj.town,
                    obObj.range,
                    obObj.rdir,
                    obObj.sect)
                # get registration status
                tempMpDict["registered"] = module_pfmm_helpers.registrationStatus(mpPwObj.plan_date, mpPwObj.registered_date)
                # Get 2c qualification status
                twoCstatusReturn = module_pfmm_helpers.twoCstatus(
                    mpPwObj.plan_date,
                    mpPwObj.assigned_date,
                    mpPwObj.registered_date)
                tempMpDict["two_c_short"] = twoCstatusReturn[0]
                # add dict to attrDict
                attrDict["mpPwDgv"].append(tempMpDict)

        # Get stewardship plan info for plans approved
        attrDict["mpPaDgv"] = []
        mpPaGidList = pcSpChildTables['management_plans.party_contact_2_guid']
        for mpPaGid in mpPaGidList:
            mpPaObj = module_pfmm_get.cls_management_plan(mpPaGid)
            # match definition query for service
            if mpPaObj.plan_type == 'Stewardship' and \
               (mpPaObj.status == 'Complete' or mpPaObj.status == 'Revised'):
                # Get related ownership_block object and child tables
                obObj = module_pfmm_get.cls_ownership_block(mpPaObj.ownership_block_guid)
                obChildTbls = module_pfmm_get.relatedRecordGlobalIds('ownership_blocks', obObj.globalid)

                # Get ownership parcels
                opGids = obChildTbls['ownership_parcels']

                # Get party_cont_own_prcl, counties, and parcel PINs
                pcopGids = []
                for opGid in opGids:
                    opObj = module_pfmm_get.cls_ownership_parcel(opGid)
                    # party_cont_own_prcl
                    opChildTbls = module_pfmm_get.relatedRecordGlobalIds('ownership_parcels', opObj.globalid)
                    pcopGids += opChildTbls['party_cont_own_prcl']

                # Get party_contact.landcontact
                pcLoGid = module_pfmm_get.lastPcopPcGid(pcopGids)
                pcLoObj = module_pfmm_get.cls_party_contact(pcLoGid)

                # start temporary dict
                tempMpDict = dict()
                # management plan attributes
                tempMpDict["management_plans.globalid"] = mpPaGid
                tempMpDict["management_plans.plan_date"] = module_pfmm_helpers.dateToYYYYMMDD(mpPaObj.plan_date)
                tempMpDict["management_plans.acres_plan"] = mpPaObj.acres_plan
                # get land contact
                tempMpDict["land_contact"] = module_pfmm_helpers.buildName(
                    pcLoObj.person_first_name,
                    pcLoObj.person_middle_name,
                    pcLoObj.person_last_name,
                    pcLoObj.person_name_prefix,
                    pcLoObj.person_name_suffix,
                    pcLoObj.spouse_name,
                    pcLoObj.business_name)
                # get plan writer
                pcPaObj = module_pfmm_get.cls_party_contact(mpPaObj.party_contact_guid)
                tempMpDict["plan_writer"] = "{0} {1} - {2}".format(
                    pcPaObj.person_first_name,
                    pcPaObj.person_last_name,
                    pcPaObj.business_name)
                # trs from owner block
                tempMpDict["pls_section"] = "T{0}N-R{1}{2}-S{3}".format(
                    obObj.town,
                    obObj.range,
                    obObj.rdir,
                    obObj.sect)
                # get registration status
                tempMpDict["registered"] = module_pfmm_helpers.registrationStatus(mpPaObj.plan_date, mpPaObj.registered_date)
                # Get 2c qualification status
                twoCstatusReturn = module_pfmm_helpers.twoCstatus(
                    mpPaObj.plan_date,
                    mpPaObj.assigned_date,
                    mpPaObj.registered_date)
                tempMpDict["two_c_short"] = twoCstatusReturn[0]
                # add dict to attrDict
                attrDict["mpPaDgv"].append(tempMpDict)

        # Get project areas for plans written
        attrDict["paDgv"] = []
        paGidList = pcSpChildTables['project_areas.party_contact_approver_guid']
        for paGid in paGidList:
            # start temporary dict
            tempPaDict = dict()
            # get objects
            paObj = module_pfmm_get.cls_project_area(paGid)
            paChildTables = module_pfmm_get.relatedRecordGlobalIds('project_areas', paGid)
            # add values to temp dict
            tempPaDict["project_areas.globalid"] = paGid
            tempPaDict["project_areas.anticipated_project_start_date"] = module_pfmm_helpers.dateToYYYYMMDD(paObj.anticipated_project_start_date)
            tempPaDict["project_areas.total_cost_share_approved"] = paObj.total_cost_share_approved
            tempPaDict["project_areas.practices_certified_date"] = module_pfmm_helpers.dateToYYYYMMDD(paObj.practices_certified_date)
            # get plan writer and add
            pcWriterObj = module_pfmm_get.cls_party_contact(paObj.party_contact_writer_guid)
            tempPaDict["writer"] = "{0} {1}".format(
                pcWriterObj.person_first_name,
                pcWriterObj.person_last_name)
            # get approver and add
            pcApproverObj = module_pfmm_get.cls_party_contact(paObj.party_contact_approver_guid)
            tempPaDict["approver"] = "{0} {1}".format(
                pcApproverObj.person_first_name,
                pcApproverObj.person_last_name)
            # get string list of project practices
            ppList = []
            ppGidList = paChildTables['project_practices']
            for ppGid in ppGidList:
                ppObj = module_pfmm_get.cls_project_practice(ppGid)
                ppList.append(ppObj.practice)
            tempPaDict["practices"] = ", ".join(sorted(set(ppList)))
            # append temp dict to out attrDict
            attrDict["paDgv"].append(tempPaDict)

    # Return
    return attrDict

def main():
    print "Content-type: application/json"
    print "Access-Control-Allow-Origin: *"
    print

    # get values from POST
    form = cgi.FieldStorage()
    spGlobalId = form.getvalue('spgid')
    callback = form.getvalue('callback')

    dictOutStart = {
        'status':"",
        'message':"",
        'timestamp':0
        }

    # check if input is a globalid
    if spGlobalId:
        if spGlobalId[:1] == '{' and spGlobalId[-1:] == '}' and len(spGlobalId) == 38:
            attrDictOut = getSpAttributesJSON(spGlobalId)
            if bool(attrDictOut):
                dictOutStart['status'] = 'OK'
                dictOutStart['message'] = 'Valid globalid received, record found.'.format(spGlobalId)
                dictOutStart['timestamp'] = int(time.time())
                dictOut = module_pfmm_helpers.mergeTwoDicts(dictOutStart, attrDictOut)
            else:
                # empty dictionary
                dictOutStart['status'] = 'ERROR'
                dictOutStart['message'] = 'Valid globalid received, but no record found.'.format(spGlobalId)
                dictOutStart['timestamp'] = int(time.time())
                dictOut = dictOutStart
        else:
            dictOutStart['status'] = 'ERROR'
            dictOutStart['message'] = 'Invalid globalid received.'.format(spGlobalId)
            dictOutStart['timestamp'] = int(time.time())
            dictOut = dictOutStart
    else:
        dictOutStart['status'] = 'ERROR'
        dictOutStart['message'] = 'No globalid received.'.format(spGlobalId)
        dictOutStart['timestamp'] = int(time.time())
        dictOut = dictOutStart

    print "{0}({1})".format(callback, json.dumps(dictOut))

if __name__ == '__main__':
    main()
