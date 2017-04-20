#-------------------------------------------------------------------------------
# Updated:     2017-02-10
#
# Name:        module_pfmm_helpers.py
# Purpose:     Helper functions for PFMWM scripts.
#
# Author:      Jeff Reinhart
#
# Created:     2017-02-10
#-------------------------------------------------------------------------------

import datetime
from calendar import isleap

def passNull(fieldValue, propertyValue):
    if fieldValue != None:
        return fieldValue
    else:
        return propertyValue

def decimalToFloat(fieldValue, propertyValue):
    if fieldValue != None:
        return float(fieldValue)
    else:
        return propertyValue

def dateToMDYYYY(dateIn):
    if dateIn == datetime.datetime(1900,1,1,0,0,0) or dateIn is None:
        dateStr = ''
    else:
        dateStr = "{dt.month}/{dt.day}/{dt.year}".format(dt = dateIn)
    return dateStr

def dateToYYYYMMDD(dateIn):
    if dateIn == datetime.datetime(1900,1,1,0,0,0) or dateIn is None:
        dateStr = ''
    else:
        dateStr = "{0}-{1}-{2}".format(dateIn.year, dateIn.strftime('%m'), dateIn.strftime('%d'))
    return dateStr

def addYears(d, years):
    """Copied from stack overflow."""
    new_year = d.year + years
    try:
        return d.replace(year=new_year)
    except ValueError:
        if (d.month == 2 and d.day == 29 and # leap day
            isleap(d.year) and not isleap(new_year)):
            return d.replace(year=new_year, day=28)
        raise

def zeroTime(d):
    return d.replace(hour=0, minute=0, second=0, microsecond=0)

def firstLastBusType(fname, lname, busType):
    return "{0} {1} - {2}".format(fname, lname, busType)

def mergeTwoDicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy. Copied from stack overflow."""
    z = x.copy()
    z.update(y)
    return z

def registrationStatus(planDate, regDate):
    regMessage = "Yes"
    today = datetime.datetime.today()
    todayBegin = zeroTime(today)
    planDateBegin = zeroTime(planDate)
    expDate = addYears(planDateBegin, 10)
    # check registered date
    if regDate == datetime.datetime(1900,1,1,0,0,0):
        regMessage = "No"
    else:
        # check if expired
        if expDate <= todayBegin:
            regMessage = "No"
    return regMessage

def twoCstatus(planDate, assignedDate, regDate):
    # variables
    twoCmessage = ""
    twoCmessageShort = ""
    today = datetime.datetime.today()
    todayBegin = zeroTime(today)
    planDateBegin = zeroTime(planDate)
    expDate = addYears(planDateBegin, 10)
    twoCregStart = datetime.datetime(todayBegin.year,1,1)
    twoCregEnd = datetime.datetime(todayBegin.year,6,15)
    submissionPeriodEnd = datetime.datetime(todayBegin.year,5,2)
    # either expiring on or before May 1 or not received by May 1 of this year
    if expDate < submissionPeriodEnd:
        twoCmessage = "No, plan will expire on or before May 1."
        twoCmessageShort = "No"
    elif assignedDate >= submissionPeriodEnd:
        twoCmessage = "No, plan was not received by May 1."
        twoCmessageShort = "No"
    # passed above two conditions, handle if in 2c registration period
    else:
        if todayBegin >= twoCregStart and todayBegin < twoCregEnd:
            # 2c registration period
            if regDate == datetime.datetime(1900,1,1,0,0,0):
                twoCmessage = "Maybe, was received by May 1, but registration is not complete."
                twoCmessageShort = "Maybe"
            else:
                twoCmessage = "Yes, was received by May 1, plan is current and registered."
                twoCmessageShort = "Yes"
        else:
            # not 2c registration period
            if regDate == datetime.datetime(1900,1,1,0,0,0) or regDate >= twoCregEnd:
                twoCmessage = "No, was received by May 1, but registration was not completed by June 14."
                twoCmessageShort = "No"
            else:
                twoCmessage = "Yes, was received by May 1, plan is current, and registration was completed by June 14."
                twoCmessageShort = "Yes"
    return [twoCmessageShort, twoCmessage]