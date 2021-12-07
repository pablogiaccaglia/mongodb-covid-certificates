import csv
import itertools
import json
import math
import operator
from _csv import reader, writer
from collections import namedtuple
from csv import DictReader, DictWriter
import random
import datetime
import utils

AddressInfo = namedtuple("AddressInfo", ["address", "city", "cityID", "country"])
HealthcareServicePersonInfo = namedtuple("HealthcareServicePersonInfo", ["role", "healthServiceID"])
EmergencyContactInfo = namedtuple("EmergencyContactInfo", ['phoneNumber', 'parent'])
VaccineLot = namedtuple("VaccineLot", ["lotID", "manufacturer", "type", "name", "productionDate", "expirationDate"])


def convertCSVDelimiter(csvPath, oldDelimiter, newDelimiter) -> None:
    """ Given a path of a CSV file, its delimiter and a new delimiter,
        creates (or overwrites) a new CSV file replacing the old delimiter
         with the new one provided as a parameter """

    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_converted' + csvPath[fileExtension:]

    with open(csvPath) as in_file, open(outputString, 'w') as out_file:
        inCSV = reader(in_file, delimiter = oldDelimiter)
        outCSV = writer(out_file, delimiter = newDelimiter)
        for row in inCSV:
            outCSV.writerow(row)


def addPhoneNumberToPeopleCSV(csvPath) -> str:
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

    return outputString


def createAddressInfo(address: str, cityInfo = utils.CityInfoTuple) -> AddressInfo:
    return AddressInfo(address = address, city = cityInfo.name, cityID = cityInfo.ID, country = cityInfo.country)


def addAddressInformationToPeopleCSV(csvPath, delimiter = ',') -> str:
    assignedAddresses = []
    tuples = []

    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_with_address_info' + csvPath[fileExtension:]

    dictReader = DictReader(open(csvPath), delimiter = delimiter)

    dictLen = len(list(dictReader))

    for _ in range(dictLen):

        address = utils.getRandomItalianAddress()

        while assignedAddresses.__contains__(address):
            address = utils.getRandomItalianAddress()

        addressInfoTuple = createAddressInfo(address = address, cityInfo = utils.getRandomItalianCityInfo())
        tuples.append(addressInfoTuple)
        assignedAddresses.append(address)

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
        row.append(addressInfoTuple.country)
        outCSV.writerow(row)

    return outputString


def addHealthcareInformationToPeopleCSV(csvPath, delimiter = ',') -> str:
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

            healthCareInfo = HealthcareServicePersonInfo(role = role, healthServiceID = healthServiceID)

            row['role'] = healthCareInfo.role
            row['healthServiceID'] = healthCareInfo.healthServiceID

            currentHealthCarePeopleAmount = currentHealthCarePeopleAmount + 1

        dictWriter.writerow(row)

    return outputString


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


def addPhoneNumberToPeopleCVS(csvPath) -> None:
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

            age = int(utils.calculateAge(utils.parseDate(row['birth date'])))

            parentRelationship = getParentRelationship(age = age,
                                                       emergencyPersonInfo = partialPersonInfo)

            row['emergency_phone_number'] = partialPersonInfo.phoneNumber
            row['emergency_parent_relationship'] = parentRelationship
            row['emergency_person_id'] = partialPersonInfo.id

        dictWriter.writerow(rowdict = row)

    return outputString


## approx 140 lots
def createsVaccineLotsList() -> list:
    vaccineLotsList = []

    for _ in range(0, 6000):
        manufacturer = utils.getRandomManufacturer()

        lotID = utils.getRandomLotNumber(manufacturer = manufacturer)
        vaccineName = utils.getVaccineName(manufacturer = manufacturer)
        vaccineType = utils.getVaccineType(manufacturer = manufacturer)
        productionAndExpirationDates = utils.getProductionAndExpirationDates()
        vaccineLot = VaccineLot(lotID = lotID,
                                manufacturer = manufacturer.value,
                                type = vaccineType,
                                name = vaccineName,
                                productionDate = productionAndExpirationDates.productionDate,
                                expirationDate = productionAndExpirationDates.expirationDate)

        vaccineLotsList.append(vaccineLot)

    return vaccineLotsList


def createCSV(headers: list, data: list, path: str) -> None:
    for entry in data:
        if len(entry) != len(headers):
            return

    with open(path, 'w') as f:
        wrt = writer(f)
        wrt.writerow(headers)
        wrt.writerows(data)


def createVaccineLotsCSV() -> None:
    vaccineLots = createsVaccineLotsList()
    headers = ["LotID", "Manufacturer", "Type", "Name", "Production Date", "Expiration Date"]
    createCSV(headers = headers, data = vaccineLots, path = utils.vaccineLotsCSVPath)


def assignVaccinesToPeople():
    lotData = csv.reader(open(utils.vaccineLotsCSVPath))
    data = sorted(lotData, key = operator.itemgetter(4), reverse = False)

    assign2DosesToPeople(lotsDict = data)
    assign1DoseToPeople(lotsDict = data)


def assign1DoseToPeople(lotsDict):
    peopleData = csv.reader(open(utils.peopleCSVPath))
    data = sorted(peopleData, key = operator.itemgetter(4), reverse = False)

    val = math.floor(len(lotsDict) * 0.25)
    maxNumOfVaccinatedWith1Dose = val
    numOfVaccinatedWith1Dose = 0
    dailyNumberOfVaccinesWith1Dose = math.floor(val / 30)
    currentDailyNumberOfVaccinesWith1Dose = 0
    currentDate = datetime.date(2021, 11, 7)

    vaccinesAmountLot = 0

    hub_serviceMapping = utils.getRandomHub_ServiceMapping(csvFilePath = utils.vaccineHub_HealthServiceMappingCSVPath)
    healthServiceID = hub_serviceMapping.HealthcareServiceID
    hubID = hub_serviceMapping.HubID

    lot = lotsDict.pop(0)

    dictWriter = DictWriter(open("datasets/final/given_vaccines.csv", 'a'),
                            fieldnames = ["PersonID",
                                          "VaccinationDate",
                                          "DoseNumber",
                                          "HealthServiceID",
                                          "HubID",
                                          "LotID",
                                          'Certification QR Code',
                                          "Disease or Agent Targeted",
                                          "Vaccine or Prophylaxis",
                                          "Vaccine Product",
                                          "Unique Certificate Identifier",
                                          "Total Series of Doses",
                                          "Country of Vaccination",
                                          "Marketing Authorization Holder",
                                          "Certificate Issuer",
                                          "Certificate valid from",
                                          "Certificate valid until",
                                          "Schema version"],
                            delimiter = ',')

    dictWriter.writeheader()

    for entry in data:

        currentDailyNumberOfVaccinesWith1Dose += 1
        numOfVaccinatedWith1Dose += 1

        if dailyNumberOfVaccinesWith1Dose < currentDailyNumberOfVaccinesWith1Dose:
            currentDate += datetime.timedelta(days = 1)
            currentDailyNumberOfVaccinesWith1Dose = 0

        if numOfVaccinatedWith1Dose > maxNumOfVaccinatedWith1Dose:
            break

        if vaccinesAmountLot > 25:  # change lot -> each lot -> 25 vials -> 150 shots
            lot = lotsDict.pop(0)
            vaccinesAmountLot = 0

            hub_serviceMapping = utils.getRandomHub_ServiceMapping(
                    csvFilePath = utils.vaccineHub_HealthServiceMappingCSVPath)
            healthServiceID = hub_serviceMapping.HealthcareServiceID
            hubID = hub_serviceMapping.HubID

        if lot[1] == "JOHNSON&JOHNSON":
            manufacturer = utils.VaccineManufacturer["JOHNSON_JOHNSON"]
        else:
            manufacturer = utils.VaccineManufacturer[lot[1]]

        row = {'PersonID':                       entry[5],
               'VaccinationDate':                currentDate,
               'DoseNumber':                     1,
               'HealthServiceID':                healthServiceID,
               'HubID':                          hubID,
               'LotID':                          lot[0],
               'Certification QR Code':          2,
               'Disease or Agent Targeted':      840539006,
               'Vaccine or Prophylaxis':         utils.getVaccineCode(manufacturer = manufacturer),
               'Vaccine Product':                utils.getVaccineProductCode(manufacturer = manufacturer),
               'Unique Certificate Identifier':  utils.getRandomUniqueCertificateIdentifier(),
               'Total Series of Doses':          2 if lot[1] != "JOHNSON&JOHNSON" else 1,
               'Country of Vaccination':         'IT',
               'Marketing Authorization Holder': utils.getVaccineManufacturerCode(manufacturer = manufacturer),
               'Certificate Issuer':             "Italian Ministry of Health",
               'Certificate valid from':         currentDate + datetime.timedelta(days = 15),
               'Certificate valid until':        currentDate + datetime.timedelta(days = 28) if lot[
                                                                                                    1] != "JOHNSON&JOHNSON"
                                                 else currentDate + datetime.timedelta(days = 270),

               'Schema version':                 '1.0.0'}

        dictWriter.writerow(row)
        vaccinesAmountLot = vaccinesAmountLot + 1


def assign2DosesToPeople(lotsDict):
    peopleData = csv.reader(open(utils.peopleCSVPath))
    data = sorted(peopleData, key = operator.itemgetter(4), reverse = False)

    val = math.floor(len(data) * 0.25)
    maxNumOfVaccinatedWith2Doses = val
    numOfVaccinatedWith2Doses = 0
    dailyNumberOfVaccinesWith2Doses = math.floor(val / 120)
    currentDailyNumberOfVaccinesWith2Doses = 0
    currentDate = datetime.date(2021, 1, 5)

    vaccinesAmountLot1 = 0
    vaccinesAmountLot2 = 0

    hub_serviceMapping = utils.getRandomHub_ServiceMapping(csvFilePath = utils.vaccineHub_HealthServiceMappingCSVPath)
    healthServiceID = hub_serviceMapping.HealthcareServiceID
    hubID = hub_serviceMapping.HubID

    lot1 = lotsDict.pop(0)
    for i in range(len(lotsDict)):
        if lotsDict[i][1] == lot1[1]:
            lot2 = lotsDict.pop(i)
            break

    dictWriter = DictWriter(open("datasets/final/given_vaccines.csv", 'w'),
                            fieldnames = ["PersonID",
                                          "VaccinationDate",
                                          "DoseNumber",
                                          "HealthServiceID",
                                          "HubID",
                                          "LotID",
                                          'Certification QR Code',
                                          "Disease or Agent Targeted",
                                          "Vaccine or Prophylaxis",
                                          "Vaccine Product",
                                          "Unique Certificate Identifier",
                                          "Total Series of Doses",
                                          "Country of Vaccination",
                                          "Marketing Authorization Holder",
                                          "Certificate Issuer",
                                          "Certificate valid from",
                                          "Certificate valid until",
                                          "Schema version"],
                            delimiter = ',')
    dictWriter.writeheader()

    for entry in data:

        dateOfSecondDose = currentDate + datetime.timedelta(days = 28)

        currentDailyNumberOfVaccinesWith2Doses += 1
        numOfVaccinatedWith2Doses += 1

        if dailyNumberOfVaccinesWith2Doses < currentDailyNumberOfVaccinesWith2Doses:
            currentDate += datetime.timedelta(days = 1)
            currentDailyNumberOfVaccinesWith2Doses = 0

        if numOfVaccinatedWith2Doses > maxNumOfVaccinatedWith2Doses:
            break

        if vaccinesAmountLot1 > 25 and vaccinesAmountLot2 > 25:  # change lot -> each lot -> 25 vials -> 150 shots
            lot1 = lotsDict.pop(0)
            vaccinesAmountLot1 = 0

            for i in range(len(lotsDict)):
                if lotsDict[i][1] == lot1[1]:
                    lot2 = lotsDict.pop(i)
                    break

            vaccinesAmountLot2 = 0

            hub_serviceMapping = utils.getRandomHub_ServiceMapping(
                    csvFilePath = utils.vaccineHub_HealthServiceMappingCSVPath)
            healthServiceID = hub_serviceMapping.HealthcareServiceID
            hubID = hub_serviceMapping.HubID

        if lot1[1] == "JOHNSON&JOHNSON":
            manufacturer = utils.VaccineManufacturer["JOHNSON_JOHNSON"]
        else:
            manufacturer = utils.VaccineManufacturer[lot1[1]]

        row = {'PersonID':                       entry[5],
               'VaccinationDate':                currentDate,
               'DoseNumber':                     1,
               'HealthServiceID':                healthServiceID,
               'HubID':                          hubID,
               'LotID':                          lot1[0],
               'Certification QR Code':          None,
               'Disease or Agent Targeted':      840539006,
               'Vaccine or Prophylaxis':         utils.getVaccineCode(manufacturer = manufacturer),
               'Vaccine Product':                utils.getVaccineProductCode(manufacturer = manufacturer),
               'Unique Certificate Identifier':  utils.getRandomUniqueCertificateIdentifier(),
               'Total Series of Doses':          2 if lot1[1] != "JOHNSON&JOHNSON" else 1,
               'Country of Vaccination':         'IT',
               'Marketing Authorization Holder': utils.getVaccineManufacturerCode(manufacturer = manufacturer),
               'Certificate Issuer':             "Italian Ministry of Health",
               'Certificate valid from':         currentDate + datetime.timedelta(days = 15),
               'Certificate valid until':        dateOfSecondDose if lot1[1] != "JOHNSON&JOHNSON"
                                                 else currentDate + datetime.timedelta(days = 270),

               'Schema version':                 '1.0.0'}

        dictWriter.writerow(row)
        vaccinesAmountLot1 = vaccinesAmountLot1 + 1

        if lot2[1] != "JOHNSON&JOHNSON":
            row = {'PersonID':                       entry[5],
                   'VaccinationDate':                dateOfSecondDose,
                   'DoseNumber':                     2,
                   'HealthServiceID':                healthServiceID,
                   'HubID':                          hubID,
                   'LotID':                          lot2[0],
                   'Certification QR Code':          None,
                   'Disease or Agent Targeted':      840539006,
                   'Vaccine or Prophylaxis':         utils.getVaccineCode(manufacturer = manufacturer),
                   'Vaccine Product':                utils.getVaccineProductCode(manufacturer = manufacturer),
                   'Unique Certificate Identifier':  utils.getRandomUniqueCertificateIdentifier(),
                   'Total Series of Doses':          2 if lot2[1] != "JOHNSON&JOHNSON" else 1,
                   'Country of Vaccination':         'IT',
                   'Marketing Authorization Holder': utils.getVaccineManufacturerCode(manufacturer = manufacturer),
                   'Certificate Issuer':             "Italian Ministry of Health",
                   'Certificate valid from':         dateOfSecondDose + datetime.timedelta(days = 3),
                   'Certificate valid until':        dateOfSecondDose + datetime.timedelta(days = 3 + 270),
                   'Schema version':                 '1.0.0'}

        dictWriter.writerow(row)
        vaccinesAmountLot2 = vaccinesAmountLot2 + 2


def findDatesOfVaccination(csvPath: str, personID: str) -> list:
    dictReader = DictReader(open(csvPath), delimiter = '')

    datesOfVaccination = []

    for row in dictReader:
        if row['PersonID'] == personID:
            datesOfVaccination.append(utils.parseDate(row['VaccinationDate']))
            if row['Vaccine Product'] == utils.VaccineProductCode.PFIZER or len(datesOfVaccination) == 2:
                break

    return sorted(datesOfVaccination)


def assignCovidTestToPeople():
    peopleData = csv.DictReader(open(utils.peopleCSVPath))

    numberOfTakenTests = [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4]

    for entry in peopleData:
        takes = random.choice(numberOfTakenTests)
        personID = entry['id']

        datesOfVaccination = findDatesOfVaccination(csvPath = 'datasets/final/given_vaccines_with_encoded_qr.csv',
                                                    personID = personID)

        for _ in range(takes):

            possibleDate1 = utils.getRandomDate(datetime.date(2020, 3, 10), datesOfVaccination[0])

            if len(datesOfVaccination) == 2:
                possibleDate2 = utils.getRandomDate(datesOfVaccination[1], datetime.date.today())
                date = random.choice([possibleDate1, possibleDate2])
            else:
                date = possibleDate1

            test = utils.getRandomCovidTest()
            isPositive = random.choice([True, False])

            hub_serviceMapping = utils.getRandomHub_ServiceMapping(
                    csvFilePath = utils.testHub_HealthServiceMappingCSVPath)
            healthServiceID = hub_serviceMapping.HealthcareServiceID
            hubID = hub_serviceMapping.HubID

            dictWriter = DictWriter(open("datasets/final/given_vaccines.csv", 'w'),
                                    fieldnames = ["PersonID",
                                                  "Test Date",
                                                  'Test Type',
                                                  'Positive'
                                                  "HealthServiceID",
                                                  "HubID",
                                                  'Certification QR Code',
                                                  "Disease or Agent Targeted",
                                                  'Test Type',
                                                  'Test Name',
                                                  'Result of the Test'
                                                  "Unique Certificate Identifier",
                                                  'Country of Testing',
                                                  "Certificate valid from",
                                                  "Certificate valid until",
                                                  "Schema version"],
                                    delimiter = ',')
            dictWriter.writeheader()

            row = {"PersonID":                      personID,
                   "Test Date":                     date,
                   'Type':                          test.value,
                   'Positive':                      isPositive,
                   "HealthServiceID":               healthServiceID,
                   "HubID":                         hubID,
                   'Certification QR Code':         None,
                   "Disease or Agent Targeted":     840539006,
                   'Test Type':                     utils.getCovidTestType(covidTest = test),
                   'Result of the Test':            utils.getCovidTestResultCode(covidTest = test,
                                                                                 isPositive = isPositive),
                   "Unique Certificate Identifier": utils.getRandomUniqueCertificateIdentifier(),
                   'Country of Testing':            'IT',

                   "Certificate valid from":        date + datetime.timedelta(
                       days = utils.getCovidTestResultWaitDays(covidTest = test))
                                                    if not isPositive else None,

                   "Certificate valid until":       date + datetime.timedelta(
                       days = utils.getCovidTestCertificateValidityDays(covidTest = test))
                                                    if not isPositive else None,

                   "Schema version":                '1.0.0'}

            dictWriter.writerow(rowdict = row)


def standardizeCSVColumns(csvPath: str, columnNames: list, delimiter = ',') -> None:
    """ Given a path of a CSV file and eventually its delimiter,
        converts each row of the given column in the CSV in a
        standard lowercase format with first letter uppercase
        creating (or overwriting) a new file """

    try:
        reader = DictReader(open(csvPath), delimiter = delimiter)
        for columnName in columnNames:
            if columnName not in reader.fieldnames:
                raise Exception(columnName + " is missing")
    except Exception as e:
        print("cannot standardize, " + str(e))
        return

    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_standardized' + csvPath[fileExtension:]

    writer = DictWriter(open(outputString, 'w'), reader.fieldnames, delimiter = delimiter)
    writer.writeheader()
    for row in reader:
        for columnName in columnNames:
            row[columnName] = row[columnName].title()
        writer.writerow(row)


def removeDuplicateRows(csvPath: str) -> None:
    """ Given the path of a CSV file,
        removes all the duplicated rows
        creating (or overwriting) a new file """

    written_entries = []

    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_no_duplicates' + csvPath[fileExtension:]

    with open(outputString, 'w') as out_file:
        with open(csvPath, 'r') as my_file:
            for line in my_file:
                if line not in written_entries:
                    out_file.write(line)
                    written_entries.append(line)


def addHealthServiceTypeToCSV(csvPath: str):
    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_with_service_type' + csvPath[fileExtension:]

    dictReader = DictReader(open(csvPath), delimiter = ",")

    dictWriter = DictWriter(open(outputString, 'w'), fieldnames = dictReader.fieldnames, delimiter = ',')
    dictWriter.writeheader()

    for row in dictReader:
        row["Type"] = row["Name"].split()[0]
        dictWriter.writerow(row)


def removeNullRows(csvPath: str, delimiter = ',') -> None:
    """ Given the path of a CSV file and eventually its delimiter,
        removes all the rows which contains at least one null value,
        creating (or overwriting) a new file"""

    try:
        dictReader = DictReader(open(csvPath), delimiter = delimiter)
    except:
        print("cannot remove null values")
        return

    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_no_nulls' + csvPath[fileExtension:]

    dictWriter = DictWriter(open(outputString, 'w'), dictReader.fieldnames, delimiter = delimiter)
    dictWriter.writeheader()

    for row in dictReader:
        nullFound = False
        for column, value in row.items():
            if value is None or value == "" or value == '-':
                nullFound = True
        if not nullFound:
            dictWriter.writerow(row)


def addRandomIDToCSV(csvPath: str) -> None:
    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_with_ID' + csvPath[fileExtension:]

    dictReader = DictReader(open(csvPath), delimiter = ",")

    headers = list(dictReader.fieldnames)
    headers.append("ID")

    dictWriter = DictWriter(open(outputString, 'w'), fieldnames = headers, delimiter = ',')
    dictWriter.writeheader()

    for row in dictReader:
        row['ID'] = utils.generateRandomString(3) + str(utils.generateRandomNumber(3))
        dictWriter.writerow(row)

    pass


def assignHubsToHealthcareServices(hubsCSVPath: str, healthcareServicesCSVPath: str, outputFilePath: str) -> None:
    hubsCSVDictReader = DictReader(open(hubsCSVPath), delimiter = ",")
    healthcareServicesCSVDictReader = DictReader(open(healthcareServicesCSVPath), delimiter = ",")

    hubsDict = {}
    healthcareServicesDict = {}

    for row in hubsCSVDictReader:

        if row['Region'] not in hubsDict:
            hubsDict[row['Region']] = []

        hubsDict[row['Region']].append(row['ID'])

    for row in healthcareServicesCSVDictReader:
        if row['Region'] not in healthcareServicesDict:
            healthcareServicesDict[row['Region']] = []

        healthcareServicesDict[row['Region']].append(row['ID'])

    dictWriter = DictWriter(open(outputFilePath, 'w'), fieldnames = ["Healthcare ID", "Hub ID"],
                            delimiter = ',')
    dictWriter.writeheader()

    for region in healthcareServicesDict:

        if region not in hubsDict:
            continue

        servicesIDsList = healthcareServicesDict[region]
        hubsIDsList = hubsDict[region]

        servicesIDsListIterator = itertools.cycle(servicesIDsList)

        servicesIDsListIterator.__next__()

        while hubsIDsList:
            row = {'Hub ID':        hubsIDsList.pop(),
                   'Healthcare ID': servicesIDsListIterator.__next__()}
            dictWriter.writerow(row)


def addQRCodesTextToCSV(csvPath: str, fieldName: str):
    dictReader = DictReader(open(csvPath), delimiter = ",")
    headers = list(dictReader.fieldnames)

    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_with_encoded_qr' + csvPath[fileExtension:]

    dictWriter = DictWriter(open(outputString, 'w'), fieldnames = headers, delimiter = ',')
    dictWriter.writeheader()

    for row in dictReader:
        row[fieldName] = utils.generateQRCode(json.dumps(row))
        dictWriter.writerow(row)


def addLocationInformationToHealthServices(csvPath: str):
    dictReader = DictReader(open(csvPath), delimiter = ",")
    headers = list(dictReader.fieldnames)

    fileExtension = csvPath.find('.csv')
    outputString = csvPath[:fileExtension] + '_with_location_info' + csvPath[fileExtension:]

    dictWriter = DictWriter(open(outputString, 'w'), fieldnames = headers, delimiter = ',')
    dictWriter.writeheader()

    for row in dictReader:

        try:
            locationInfo = utils.getLocationInfo(gmaps = utils.gmapsClient,
                                                 location = row['Name'] + " " + row['Region'])

            row["Address"] = locationInfo.formattedAddress
            row["City"] = locationInfo.city
            row["Postal Code"] = locationInfo.postalCode
            row["Longitude"] = locationInfo.longitude
            row["Latitude"] = locationInfo.latitude

        except Exception as e:
            print(str(e))
            pass

        dictWriter.writerow(row)


if __name__ == '__main__':
    #  path1 = addPhoneNumberToPeopleCSV(utils.peopleCSVPath)
    #  path2 = addAddressInformationToPeopleCSV(path1)
    #  path3 = addHealthcareInformationToPeopleCSV(path2)
    #  addEmergencyContactInfoToPeopleCSV(path3)
    # createVaccineLotsCSV()
    # convertCSVDelimiter(csvPath = "datasets/original/asl italia 3.csv", oldDelimiter = ';', newDelimiter = ',')
    # headers = ['denominazione_struttura']
    # standardizeCSVColumns(csvPath ="/Users/pablo/Desktop/SMBUDMongo/datasets/original/punti-somministrazione-tipologia.csv", columnNames = headers)
    # removeDuplicateRows(csvPath = "/Users/pablo/Desktop/SMBUDMongo/datasets/converted/punti-somministrazione-tipologia_standardized.csv")
    # addHealthServiceTypeToCSV()
    # convertCSVDelimiter(csvPath = "datasets/final/italian pharmacies.csv", oldDelimiter = ';', newDelimiter = ',')
    # removeDuplicateRows(csvPath = "datasets/final/italian pharmacies_converted.csv")
    # removeNullRows(csvPath = "datasets/final/italian pharmacies_converted_no_duplicates.csv")
    # convertCSVDelimiter(csvPath = "datasets/final/punti-somministrazione-tipologia_standardized_no_duplicates.csv", oldDelimiter = ';', newDelimiter = ',')

    # addRandomIDToCSV("datasets/final/asl italia 3_converted_standardized_no_duplicates_with_service_type.csv")

    """
        assignHubsToHealthcareServices(
                hubsCSVPath = "datasets/final/punti-somministrazione-tipologia_standardized_no_duplicates_with_ID.csv",
                healthcareServicesCSVPath = "datasets/final/asl italia 3_converted_standardized_no_duplicates_with_service_type_with_ID.csv",
                outputFilePath = "datasets/final/vaccineHubs-services id mapping.csv")
    
        assignHubsToHealthcareServices(
                hubsCSVPath = "datasets/final/italian pharmacies_converted_no_duplicates_no_nulls_with_ID.csv",
                healthcareServicesCSVPath = "datasets/final/asl italia 3_converted_standardized_no_duplicates_with_service_type_with_ID.csv",
                outputFilePath = "datasets/final/TestHubs-services id mapping.csv")
                
                """

    # createVaccineLotsCSV()
    # assignVaccinesToPeople()
    # addQRCodesTextToCSV(csvPath = "datasets/final/given_vaccines.csv", fieldName = 'Certification QR Code')
    addLocationInformationToHealthServices(
        csvPath = "datasets/final/punti-somministrazione-tipologia_standardized_no_duplicates_with_ID.csv")
