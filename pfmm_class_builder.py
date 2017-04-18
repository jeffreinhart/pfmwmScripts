'''Builds class for table. Table county_coun needs updates after run because
it doesn't have a globalid.'''

import arcpy

def printClassDefinitionScript(dataset):
    skipList = ['objectid', 'shape', 'st_area(shape)', 'st_length(shape)']

    fieldList = arcpy.ListFields(dataset)

    datasetDesc = arcpy.Describe(dataset)

    datasetShortName = datasetDesc.baseName[14:]

    datasetFormalName = ' '.join(datasetShortName.split("_")).title()

    # start class
    classScript = ''
    classScript += "class cls_{0}:\n".format(datasetShortName[:-1])
    classScript += "    '''PFM {0} record.'''\n".format(datasetFormalName)
    classScript += "    def __init__(self, globalId = '', guid = ''):\n"
    classScript += "        self.globalIdExists = False\n"
    classScript += "        self.fieldList = [\n"

    # build self.fieldList
    for field in fieldList:
        if field.baseName not in skipList:
            classScript += "            '{0}',\n".format(field.baseName)

    # close braces on the field list
    classScript +=  "             ]\n"

    # build query
    classScript +=  "        self.query = 'select {0} from "+datasetShortName+"_evw where globalid = %s'.format(', '.join(self.fieldList))\n"

    # build each property
    for field in fieldList:
        if field.baseName not in skipList:
            if field.baseName[-4:] == "date":
                classScript += "        self.{0} = datetime.datetime(1900,1,1,0,0,0)\n".format(field.baseName)
            elif field.baseName == "globalid":
                classScript += "        self.{0} = ''\n".format(field.baseName)
            elif field.type in ["Double", "SmallInteger"]:
                classScript += "        self.{0} = 0\n".format(field.baseName)
            else:
                classScript += "        self.{0} = ''\n".format(field.baseName)

    classScript += "        conn = psycopg2.connect(dsn)\n"
    classScript += "        with conn.cursor() as curs:\n"
    classScript += "            curs.execute(self.query, [globalId])\n"
    classScript += "            for row in curs:\n"
    classScript += "                self.globalIdExists = True\n"

    # build each property
    index = 0
    for field in fieldList:
        if field.baseName not in skipList:
            if field.type == "Double":
                classScript += "                self.{0} = module_pfmm_helpers.decimalToFloat(row[{1}], self.{0})\n".format(field.baseName, str(index))
            else:
                classScript += "                self.{0} = module_pfmm_helpers.passNull(row[{1}], self.{0})\n".format(field.baseName, str(index))
            index += 1

    classScript += "        conn.close()\n"

    print classScript

datasetList = [
    r'P:\FOR\FORIST\PFM\dev10_2\dnrgdrs-prod1-pg-dc-pfmm.sde\pfmm_dev.pfmm.party_contacts',
    r'P:\FOR\FORIST\PFM\dev10_2\dnrgdrs-prod1-pg-dc-pfmm.sde\pfmm_dev.pfmm.spatial\pfmm_dev.pfmm.management_plans',
    r'P:\FOR\FORIST\PFM\dev10_2\dnrgdrs-prod1-pg-dc-pfmm.sde\pfmm_dev.pfmm.spatial\pfmm_dev.pfmm.ownership_blocks',
    r'P:\FOR\FORIST\PFM\dev10_2\dnrgdrs-prod1-pg-dc-pfmm.sde\pfmm_dev.pfmm.spatial\pfmm_dev.pfmm.ownership_parcels',
    r'P:\FOR\FORIST\PFM\dev10_2\dnrgdrs-prod1-pg-dc-pfmm.sde\pfmm_dev.pfmm.party_cont_own_prcl',
    r'P:\FOR\FORIST\PFM\dev10_2\dnrgdrs-prod1-pg-dc-pfmm.sde\pfmm_dev.pfmm.party_cont_own_blks',
    r'P:\FOR\FORIST\PFM\dev10_2\dnrgdrs-prod1-pg-dc-pfmm.sde\pfmm_dev.pfmm.contact_events',
    r'P:\FOR\FORIST\PFM\dev10_2\dnrgdrs-prod1-pg-dc-pfmm.sde\pfmm_dev.pfmm.spatial\pfmm_dev.pfmm.project_areas',
    r'P:\FOR\FORIST\PFM\dev10_2\dnrgdrs-prod1-pg-dc-pfmm.sde\pfmm_dev.pfmm.spatial\pfmm_dev.pfmm.project_practices'
    r'P:\FOR\FORIST\PFM\dev10_2\dnrgdrs-prod1-pg-dc-pfmm.sde\pfmm_dev.pfmm.county_coun',
    ]

for dataset in datasetList:
    printClassDefinitionScript(dataset)