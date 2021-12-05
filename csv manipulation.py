from _csv import reader, writer
from collections import namedtuple, OrderedDict
from csv import DictReader, DictWriter
from random import random
from typing import Union

import utils

addressInfo = namedtuple("AddressInfo", ["address", "city", "cityID", "state"])
healthcareServicePersonInfo = namedtuple("HealthcareServicePersonInfo", ["role", "healthServiceID"])
emergencyContactInfo = namedtuple("EmergencyContactInfo", ['phoneNumber', 'parent'])


def addPhoneNumberToPeopleCSV(csvPath) -> None:
    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_with_phone_numbers' + csvPath[fileExtension:]

    inCSV = reader(open(csvPath, 'r'))
    outCSV = writer(open(outputString, 'w'))
    headers = next(inCSV)
    headers.append("phone_number")
    outCSV.writerow(headers)

    for row in inCSV:
        row.append(utils.getRandomPhoneNumber())
        outCSV.writerow(row)


def createAddressInfo(address: str, row: Union[dict[str, str], OrderedDict[str, str]]) -> addressInfo:
    return addressInfo(address = address, city = row['city'], cityID = row['id'], state = "iso3")


def addAddressInformationToPeopleCSV(csvPath, delimiter = ',') -> None:
    assignedAddresses = []
    tuples = []

    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_with_address_info' + csvPath[fileExtension:]

    dictReader = DictReader(open(csvPath), delimiter = delimiter)

    for row in dictReader:

        address = utils.getRandomItalianAddress()

        while assignedAddresses.__contains__(o = address):
            address = utils.getRandomItalianAddress()

        addressInfoTuple = createAddressInfo(address = address, row = row)
        tuples.append(addressInfoTuple)

    inCSV = reader(open(csvPath, 'r'))
    outCSV = writer(open(outputString, 'w'))
    headers = next(inCSV)
    headers.append("address")
    headers.append("city")
    headers.append("cityID")
    headers.append("state")
    outCSV.writerow(headers)

    for row in inCSV:
        addressInfoTuple = tuples.pop()
        row.append(addressInfoTuple.address)
        row.append(addressInfoTuple.city)
        row.append(addressInfoTuple.cityID)
        row.append(addressInfoTuple.state)
        outCSV.writerow(row)


def addHealthcareInformationToPeopleCSV(csvPath, delimiter = ',') -> None:
    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_with_healtcare_info' + csvPath[fileExtension:]

    dictReader = DictReader(open(csvPath), delimiter = delimiter)

    headers = list(dictReader.fieldnames)
    headers.append("role")
    headers.append("healthServiceID")

    dictWriter = DictWriter(open(outputString, 'w'), headers, delimiter = delimiter)
    dictWriter.writeheader()

    maxHealthCarePeopleAmount = 1000
    currentHealthCarePeopleAmount = 0

    for row in dictReader:

        birthDate = utils.parseDate(row['birth date'])
        age = utils.calculateAge(birthDate)

        if 25 < age < 65 and currentHealthCarePeopleAmount < maxHealthCarePeopleAmount:
            healthServiceID = utils.generateRandomHealthcareWorkerID()
            role = random.choice(["nurse", "doctor"])

            healthCareInfo = healthcareServicePersonInfo(role = role, healthServiceID = healthServiceID)

            row['role'] = healthCareInfo.role
            row['healthServiceID'] = healthCareInfo.healthServiceID

            currentHealthCarePeopleAmount = currentHealthCarePeopleAmount + 1

        dictWriter.writerow(row)


def getParentRelationship(age: int, emergencyPersonInfo: utils.partialPersonInfo):
    ageGap = abs(age - emergencyPersonInfo.age)

    if ageGap <= 10:

        if utils.generateRandomNumber(5) % 2 == 0:
            return "spouse"
        else:

            if utils.generateRandomNumber(5) % 2 == 0:
                return "sibling"
            else:
                return "friend"

    if emergencyPersonInfo.age - age >= 25:

        if emergencyPersonInfo.sex == "male":
            return "father"
        else:
            return "mother"

    if age - emergencyPersonInfo.age > 20:

        if utils.generateRandomNumber(5) % 2 == 0:
            return "child"
        else:
            if utils.generateRandomNumber(5) % 2 == 0:
                return "nephew"
            else:
                return "friend"

    if emergencyPersonInfo.age - age > 20:

        if utils.generateRandomNumber(5) % 2 == 0:
            return "child"
        else:
            if utils.generateRandomNumber(5) % 2 == 0:

                if emergencyPersonInfo.sex == "male":
                    return "uncle"
                else:
                    return "aunt"
            else:
                return "friend"

    return "friend"


def addEmergencyContactInfoToPeopleCSV(csvPath, delimiter = ',') -> None:
    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_with_emergency_contact_info' + csvPath[fileExtension:]

    dictReader = DictReader(open(csvPath), delimiter = delimiter)

    headers = list(dictReader.fieldnames)
    headers.append("emergency_phone_number")
    headers.append("emergency_parent_relationship")
    headers.append("emergency_person_id")

    dictWriter = DictWriter(open(outputString, 'w'), headers, delimiter = delimiter)
    dictWriter.writeheader()

    for row in dictReader:

        if utils.generateRandomNumber(10) % 2 == 0:
            pass
        else:

            partialPersonInfo = utils.getRandomPersonPartialInfo()

            while partialPersonInfo.id == row['id']:
                partialPersonInfo = utils.getRandomPersonPartialInfo()

            phoneNumber = utils.getRandomPhoneNumber()

            parentRelationship = getParentRelationship(age = int(row['age']),
                                                       emergencyPersonInfo = partialPersonInfo)



            pass

        dictWriter.writerow(row)
