#-------------------------------------------------------------------------------
# Updated:     2017-04-18
#
# Name:        get_project_area_attributes_json.py
#
# Purpose:     Get all attributes for a project_area polygon that are needed
#              in the PFMWM from related records in PFMM.
#
# Author:      Jeff Reinhart
#
# Created:     2017-04-18
#-------------------------------------------------------------------------------


import module_pfmm_get, module_pfmm_helpers
import json, cgi, datetime, time

def getProjectAreaAttributesJSON(paGlobalId):
    # Output
    attrDict = dict()

    # Get project_area object
    paObj = module_pfmm_get.cls_project_area(paGlobalId)

    if paObj.globalIdExists:
        # Get party_contact.applicant
        pcAppObj = module_pfmm_get.cls_party_contact(paObj.party_contact_applicant_guid)

        # Get party_contact.plan_writer
        pcPwObj = module_pfmm_get.cls_party_contact(paObj.party_contact_writer_guid)

        # Get party_contact.approver
        pcApprObj = module_pfmm_get.cls_party_contact(paObj.party_contact_approver_guid)

        # Get party_contact.certifier
        pcCertObj = module_pfmm_get.cls_party_contact(paObj.party_contact_certifier_guid)

        # Build list for html for project_area
        attrDict["html"] = [
            {
                "type": "hidden",
                "name": "project_areas.globalid",
                "value": paObj.globalid
            },
            {
                "type": "hidden",
                "name": "party_contacts.globalid.applicant",
                "value": pcAppObj.globalid
            },
            {
                "type": "hidden",
                "name": "party_contacts.globalid.writer",
                "value": pcPwObj.globalid
            },
            {
                "type": "hidden",
                "name": "party_contacts.globalid.approver",
                "value": pcApprObj.globalid
            },
            {
                "type": "hidden",
                "name": "party_contacts.globalid.certifier",
                "value": pcCertObj.globalid
            },
            {
                "caption": "Project Applicant First Name",
                "type": "text",
                "name": "party_contacts.person_first_name.applicant",
                "value": pcAppObj.person_first_name
            },
            {
                "caption": "Project Applicant Last Name",
                "type": "text",
                "name": "party_contacts.person_last_name.applicant",
                "value": pcAppObj.person_last_name
            },
            {
                "caption": "Project Applicant Partner First Name",
                "type": "text",
                "name": "party_contacts.spouse_name.landcontact",
                "value": pcAppObj.spouse_name
            },
            {
                "caption": "Project Applicant Business Name",
                "type": "text",
                "name": "party_contacts.business_name.landcontact",
                "value": pcAppObj.business_name
            },
            {
                "caption": "Project Applicant Street Address",
                "type": "text",
                "name": "party_contacts.address_line_1.landcontact",
                "value": pcAppObj.address_line_1
            },
            {
                "caption": "Project Applicant City",
                "type": "text",
                "name": "party_contacts.city.landcontact",
                "value": pcAppObj.city
            },
            {
                "caption": "Project Applicant State",
                "type": "text",
                "name": "party_contacts.state_provice_short_name_code.landcontact",
                "value": pcAppObj.state_provice_short_name_code
            },
            {
                "caption": "Project Applicant Zip",
                "type": "text",
                "name": "party_contacts.postal_code.landcontact",
                "value": pcAppObj.postal_code
            },
            {
                "caption": "Project Applicant Do Not Mail",
                "type": "text",
                "name": "party_contacts.do_not_mail.landcontact",
                "value": pcAppObj.do_not_mail
            },
            {
                "caption": "Project Applicant Phone 1",
                "type": "text",
                "name": "party_contacts.phone_line_1.landcontact",
                "value": pcAppObj.phone_line_1
            },
            {
                "caption": "Project Plan Writer",
                "type": "text",
                "name": "planwriter",
                "value": module_pfmm_helpers.firstLastBusType(
                    pcPwObj.person_first_name,
                    pcPwObj.person_last_name,
                    pcPwObj.business_type)
            },
            {
                "caption": "Project Plan Delivered Date",
                "type": "text",
                "name": "project_areas.project_plan_delivered_date",
                "datepicker": {
                    "minDate": "01/01/1900"
                },
                "value": module_pfmm_helpers.dateToMDYYYY(paObj.project_plan_delivered_date)
            },
            {
                "caption": "GIS Acres",
                "type": "number",
                "name": "project_areas.acres_gis",
                "value": paObj.acres_gis
            },
            {
                "caption": "Anticipated Start Date",
                "type": "text",
                "name": "project_areas.anticipated_project_start_date",
                "datepicker": {
                    "minDate": "01/01/1900"
                },
                "value": module_pfmm_helpers.dateToMDYYYY(paObj.anticipated_project_start_date)
            },
            {
                "caption": "Completion Date",
                "type": "text",
                "name": "project_areas.completion_date",
                "datepicker": {
                    "minDate": "01/01/1900"
                },
                "value": module_pfmm_helpers.dateToMDYYYY(paObj.completion_date)
            },
            {
                "caption": "Canceled Date",
                "type": "text",
                "name": "project_areas.canceled_date",
                "datepicker": {
                    "minDate": "01/01/1900"
                },
                "value": module_pfmm_helpers.dateToMDYYYY(paObj.canceled_date)
            },
            {
                "caption": "Reason for Canceling",
                "type": "text",
                "name": "project_areas.reason_for_canceling",
                "value": paObj.reason_for_canceling
            },
            {
                "caption": "Comments",
                "type": "text",
                "name": "project_areas.comments",
                "value": paObj.comments
            },
            {
                "caption": "Cost Share Request Approved Date",
                "type": "text",
                "name": "project_areas.request_approved_date",
                "datepicker": {
                    "minDate": "01/01/1900"
                },
                "value": module_pfmm_helpers.dateToMDYYYY(paObj.request_approved_date)
            },
            {
                "caption": "Approved By",
                "type": "text",
                "name": "approver",
                "value": module_pfmm_helpers.firstLastBusType(
                    pcApprObj.person_first_name,
                    pcApprObj.person_last_name,
                    pcApprObj.business_type)
            },
            {
                "caption": "Total Cost Share Approved",
                "type": "number",
                "name": "project_areas.total_cost_share_approved",
                "value": paObj.total_cost_share_approved
            },
            {
                "caption": "Completion Deadline Date",
                "type": "text",
                "name": "project_areas.completion_deadline_date",
                "datepicker": {
                    "minDate": "01/01/1900"
                },
                "value": module_pfmm_helpers.dateToMDYYYY(paObj.completion_deadline_date)
            },
            {
                "caption": "Practices Certified Date",
                "type": "text",
                "name": "project_areas.practices_certified_date",
                "datepicker": {
                    "minDate": "01/01/1900"
                },
                "value": module_pfmm_helpers.dateToMDYYYY(paObj.practices_certified_date)
            },
            {
                "caption": "Certified By",
                "type": "text",
                "name": "certifier",
                "value": module_pfmm_helpers.firstLastBusType(
                    pcCertObj.person_first_name,
                    pcCertObj.person_last_name,
                    pcCertObj.business_type)
            },
            {
                "caption": "Total Cost Share To Be Paid",
                "type": "number",
                "name": "project_areas.total_cost_share_to_be_paid",
                "value": paObj.total_cost_share_to_be_paid
            }
        ]

        # Get project practices for data grid view
        attrDict["ppDgv"] = []
        paChildTables = module_pfmm_get.relatedRecordGlobalIds('project_areas', paGlobalId)
        ppGidList = paChildTables['project_practices']
        for ppGid in ppGidList:
            # start temporary dict
            tempCeDict = dict()
            # get object
            ppObj = module_pfmm_get.cls_project_practice(ppGid)
            # add values to temp dict
            tempCeDict["project_practices.globalid"] = ppObj.globalid
            tempCeDict["project_practices.anticipated_practice_start_date"] = module_pfmm_helpers.dateToYYYYMMDD(ppObj.anticipated_practice_start_date)
            tempCeDict["project_practices.practice"] = ppObj.practice
            tempCeDict["project_practices.component"] = ppObj.component
            tempCeDict["project_practices.task"] = ppObj.task
            tempCeDict["project_practices.subtask"] = ppObj.subtask
            tempCeDict["project_practices.component_unit"] = ppObj.component_unit
            tempCeDict["project_practices.cost_per_unit"] = ppObj.cost_per_unit
            tempCeDict["project_practices.cost_share_rate"] = ppObj.cost_share_rate
            tempCeDict["project_practices.proposed_component_amount"] = ppObj.proposed_component_amount
            tempCeDict["project_practices.estimated_total_cost"] = ppObj.estimated_total_cost
            tempCeDict["project_practices.completion_date"] = module_pfmm_helpers.dateToYYYYMMDD(ppObj.completion_date)
            tempCeDict["project_practices.completed_component_amount"] = ppObj.completed_component_amount
            tempCeDict["project_practices.requesting_cost_share"] = ppObj.requesting_cost_share
            tempCeDict["project_practices.cost_shares_recommended"] = ppObj.cost_shares_recommended
            tempCeDict["project_practices.cost_shares_earned"] = ppObj.cost_shares_earned
            tempCeDict["project_practices.comments"] = ppObj.comments
            # append to attrDict
            attrDict["ppDgv"].append(tempCeDict)

    # Return
    return attrDict

def main():
    print "Content-type: application/json"
    print "Access-Control-Allow-Origin: *"
    print

    form = cgi.FieldStorage()
    paGlobalId = form.getvalue('pagid')
    callback = form.getvalue('callback')

    dictOutStart = {
        'status':"",
        'message':"",
        'timestamp':0
        }

    # check if input is a globalid
    if paGlobalId:
        if paGlobalId[:1] == '{' and paGlobalId[-1:] == '}' and len(paGlobalId) == 38:
            attrDictOut = getProjectAreaAttributesJSON(paGlobalId)
            if bool(attrDictOut):
                dictOutStart['status'] = 'OK'
                dictOutStart['message'] = 'Valid globalid received, record found.'.format(paGlobalId)
                dictOutStart['timestamp'] = int(time.time())
                dictOut = module_pfmm_helpers.mergeTwoDicts(dictOutStart, attrDictOut)
            else:
                # empty dictionary
                dictOutStart['status'] = 'ERROR'
                dictOutStart['message'] = 'Valid globalid received, but no record found.'.format(paGlobalId)
                dictOutStart['timestamp'] = int(time.time())
                dictOut = dictOutStart
        else:
            dictOutStart['status'] = 'ERROR'
            dictOutStart['message'] = 'Invalid globalid received.'.format(paGlobalId)
            dictOutStart['timestamp'] = int(time.time())
            dictOut = dictOutStart
    else:
        dictOutStart['status'] = 'ERROR'
        dictOutStart['message'] = 'No globalid received.'.format(paGlobalId)
        dictOutStart['timestamp'] = int(time.time())
        dictOut = dictOutStart

    print "{0}({1})".format(callback, json.dumps(dictOut))

if __name__ == '__main__':
    main()