#-------------------------------------------------------------------------------
# Updated:     2017-04-14
#
# Name:        get_lc_attributes_json.py
#
# Purpose:     Get pertinent attributes for a party_contact land contact record
#              and related records for data grids.
#
# Author:      Jeff Reinhart
#
# Created:     2017-02-08
#-------------------------------------------------------------------------------

import module_pfmm_get, module_pfmm_helpers
import json, cgi, datetime, time

def getLcAttributesJSON(lcGid):
    # Dictionary to pass to JSON output
    attrDict = dict()

    # Get party_contact.landcontact
    pcLoObj = module_pfmm_get.cls_party_contact(lcGid)

    if pcLoObj.globalIdExists:
        # Build list for html for record attributes
        attrDict["html"] = [
            {
                "type": "hidden",
                "name": "party_contacts.globalid.landcontact",
                "value": pcLoObj.globalid
            },
            {
                "caption": "Land Contact First Name",
                "type": "text",
                "name": "party_contacts.person_first_name.landcontact",
                "value": pcLoObj.person_first_name
            },
            {
                "caption": "Land Contact Last Name",
                "type": "text",
                "name": "party_contacts.person_last_name.landcontact",
                "value": pcLoObj.person_last_name
            },
            {
                "caption": "Land Contact Partner First Name",
                "type": "text",
                "name": "party_contacts.spouse_name.landcontact",
                "value": pcLoObj.spouse_name
            },
            {
                "caption": "Land Contact Business Name",
                "type": "text",
                "name": "party_contacts.business_name.landcontact",
                "value": pcLoObj.business_name
            },
            {
                "caption": "Land Contact Street Address",
                "type": "text",
                "name": "party_contacts.address_line_1.landcontact",
                "value": pcLoObj.address_line_1
            },
            {
                "caption": "Land Contact City",
                "type": "text",
                "name": "party_contacts.city.landcontact",
                "value": pcLoObj.city
            },
            {
                "caption": "Land Contact State",
                "type": "text",
                "name": "party_contacts.state_provice_short_name_code.landcontact",
                "value": pcLoObj.state_provice_short_name_code
            },
            {
                "caption": "Land Contact Zip",
                "type": "text",
                "name": "party_contacts.postal_code.landcontact",
                "value": pcLoObj.postal_code
            },
            {
                "caption": "Land Contact Do Not Mail",
                "type": "text",
                "name": "party_contacts.do_not_mail.landcontact",
                "value": pcLoObj.do_not_mail
            },
            {
                "caption": "Land Contact Phone 1",
                "type": "text",
                "name": "party_contacts.phone_line_1.landcontact",
                "value": pcLoObj.phone_line_1
            }
        ]

        # Get stewardship plan info through owner block
        attrDict["mpDgv"] = []
        pcLoChildTables = module_pfmm_get.relatedRecordGlobalIds('party_contacts', lcGid)
        pcobGidList = pcLoChildTables['party_cont_own_blks']
        obGidList = []
        for pcobGid in pcobGidList:
            pcobObj = module_pfmm_get.cls_party_cont_own_blk(pcobGid)
            obGidList.append(pcobObj.ownership_block_guid)
        for obGid in obGidList:
            isOwner = "No" # assume not owner until confirmed
            countyList = []
            # get ownership_block and child tables
            obObj = module_pfmm_get.cls_ownership_block(obGid)
            obChildTables = module_pfmm_get.relatedRecordGlobalIds('ownership_blocks', obGid)
            # get ownership parcels
            opGidList = obChildTables['ownership_parcels']
            for opGid in opGidList:
                # get ownership_parcel and child tables
                opObj = module_pfmm_get.cls_ownership_parcel(opGid)
                opChildTables = module_pfmm_get.relatedRecordGlobalIds('ownership_parcels', opGid)
                # append county to list
                counObj = module_pfmm_get.cls_county_coun(opObj.coun)
                countyList.append(counObj.cty_name)
                # check if owner is same
                pcopGidList = opChildTables['party_cont_own_prcl']
                pcOnwerGid = module_pfmm_get.lastPcopPcGid(pcopGidList)
                if pcOnwerGid == lcGid:
                    isOwner = "Yes"
            # get management plans
            mpGidList = obChildTables['management_plans']
            for mpGid in mpGidList:
                mpObj = module_pfmm_get.cls_management_plan(mpGid)
                if mpObj.globalIdExists:
                    # match definition query for service
                    if mpObj.plan_type == 'Stewardship' and \
                       (mpObj.status == 'Complete' or mpObj.status == 'Revised'):
                        # start temporary dict
                        tempMpDict = dict()
                        # county list to string
                        tempMpDict["counties"] = ", ".join(sorted(set(countyList)))
                        # management plan attributes
                        tempMpDict["management_plans.globalid"] = mpGid
                        tempMpDict["management_plans.plan_date"] = module_pfmm_helpers.dateToYYYYMMDD(mpObj.plan_date)
                        tempMpDict["management_plans.acres_plan"] = mpObj.acres_plan
                        expirationDate = module_pfmm_helpers.addYears(mpObj.plan_date, 10)
                        tempMpDict["expiration_date"] = module_pfmm_helpers.dateToYYYYMMDD(expirationDate)
                        # get plan writer
                        pcPwObj = module_pfmm_get.cls_party_contact(mpObj.party_contact_guid)
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
                        tempMpDict["registered"] = module_pfmm_helpers.registrationStatus(mpObj.plan_date, mpObj.registered_date)
                        # Get 2c qualification status
                        twoCstatusReturn = module_pfmm_helpers.twoCstatus(
                            mpObj.plan_date,
                            mpObj.assigned_date,
                            mpObj.registered_date)
                        tempMpDict["two_c_short"] = twoCstatusReturn[0]
                        # add if is owner
                        tempMpDict["is_owner"] = isOwner
                        # add dict to attrDict
                        attrDict["mpDgv"].append(tempMpDict)

        # Get contact_events
        attrDict["ceDgv"] = []
        contactEventGidList = pcLoChildTables['contact_events.party_contact_1_guid']
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
            # get DNR party contact and add
            pcDnrObj = module_pfmm_get.cls_party_contact(contactEventObj.party_contact_2_guid)
            tempCeDict["dnr_staff"] = "{0} {1}".format(
                pcDnrObj.person_first_name,
                pcDnrObj.person_last_name)
            # get Partner Forester party contact and add
            pcPfObj = module_pfmm_get.cls_party_contact(contactEventObj.party_contact_3_guid)
            tempCeDict["partner_forester"] = "{0} {1}".format(
                pcPfObj.person_first_name,
                pcPfObj.person_last_name)
            attrDict["ceDgv"].append(tempCeDict)

        # Get project_areas
        attrDict["paDgv"] = []
        paGidList = pcLoChildTables['project_areas.party_contact_applicant_guid']
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
    lcGlobalId = form.getvalue('lcgid')
    callback = form.getvalue('callback')

    dictOutStart = {
        'status':"",
        'message':"",
        'timestamp':0
        }

    # check if input is a globalid
    if lcGlobalId:
        if lcGlobalId[:1] == '{' and lcGlobalId[-1:] == '}' and len(lcGlobalId) == 38:
            attrDictOut = getLcAttributesJSON(lcGlobalId)
            if bool(attrDictOut):
                dictOutStart['status'] = 'OK'
                dictOutStart['message'] = 'Valid globalid received, record found.'.format(lcGlobalId)
                dictOutStart['timestamp'] = int(time.time())
                dictOut = module_pfmm_helpers.mergeTwoDicts(dictOutStart, attrDictOut)
            else:
                # empty dictionary
                dictOutStart['status'] = 'ERROR'
                dictOutStart['message'] = 'Valid globalid received, but no record found.'.format(lcGlobalId)
                dictOutStart['timestamp'] = int(time.time())
                dictOut = dictOutStart
        else:
            dictOutStart['status'] = 'ERROR'
            dictOutStart['message'] = 'Invalid globalid received.'.format(lcGlobalId)
            dictOutStart['timestamp'] = int(time.time())
            dictOut = dictOutStart
    else:
        dictOutStart['status'] = 'ERROR'
        dictOutStart['message'] = 'No globalid received.'.format(lcGlobalId)
        dictOutStart['timestamp'] = int(time.time())
        dictOut = dictOutStart

    print "{0}({1})".format(callback, json.dumps(dictOut))

if __name__ == '__main__':
    main()
