import cv2
import pytesseract
import re
import datetime
import json
from getData import config


# validate date format for extraction
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d/%m/%Y')
        return True
    except ValueError:
        return False


def extraction(bank):
    try:
        path = config.ImagePath + bank + '.png'
        img = cv2.imread(path)
        t = pytesseract.image_to_string(img)
        fields = {}
        m = re.findall("CR[ ]*No. [\d—-]+", t)
        if m:
            fields['CrNo'] = m[0]
        m = re.findall("Commercial[ ]*Name[ ]*\(English\)[ ].*", t)
        if m:
            fields['Name'] = m[0]
        t = t.replace("\n", ":")
        refactor_string = t.split("Company Information:", 1)[1]
        while refactor_string.find(":: ::") != -1:
            refactor_string = refactor_string.replace(":: ::", "::")
        refactor_string = refactor_string.replace("::", ":")
        y = refactor_string.split(":")
        for i in range(0, len(y)):
            if 'Nationality' in y[i]:
                s = y[i].split(" ")
                fields['Status'] = s[0]
            elif 'Expiry Date' in y[i]:
                s = y[i].split(" ")
                fields['RegistrationDate'] = s[0]
            elif 'Financial Year' in y[i]:
                s = y[i].split(" ")
                fields['CompanyPeriod'] = s[0]
            elif validate(y[i]):
                fields['Nationality'] = y[i - 1]
                fields['ExpiryDate'] = y[i]

        json_obj = json.dumps(fields)
        return json_obj

    except Exception as e:
        fields = {'error': "Error in getData function : " + getattr(e, 'message', repr(e)),
                  'cause': "Possible cause column name different then learning document Check name of bank should be " \
                           "same as in list(Case sensitive)", 'Bank-list': config.bank_list}
        json_obj = json.dumps(fields)
        return json_obj
