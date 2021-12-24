from csv import DictReader
from datetime import datetime
from typing import Optional
from pymongo import MongoClient
import utils
from bson.objectid import ObjectId
import ast


class MongoDB(MongoClient):

    def __init__(self, connectionURI) -> None:
        super(MongoDB, self).__init__(connectionURI, connect = False)
        # to see connection status
        print(str(self.stats))

    def __handleDateParsing(self, date: str) -> Optional[datetime]:
        if date == '':
            return None
        else:
            return utils.parseDate(date = date)

    def __handleIntParsing(self, val: str) -> Optional[int]:

        if val == '':
            return None

        else:
            return int(val)

    def __handleFloatParsing(self, val: str) -> Optional[float]:

        if val == '':
            return None

        else:
            return float(val.replace(',', ''))

    def __handleEmptyString(self, val: str) -> Optional[str]:

        if val == "":
            return None
        else:
            return val

    def __createDBRef(self, collectionName: str, objectId: str, db) -> Optional[dict]:

        if collectionName is None or objectId is None or db is None:
            return None

        ref = {
            "$ref": collectionName,
            "$id":  ObjectId(objectId),
            "$db":  db.name
        }

        return ref

    def __createPersonDocuments(self, db) -> None:

        personCollection = db['person']

        dictReaderPeoples = DictReader(open(utils.peopleCSVPathFinal), delimiter = ",")
        # dictReaderTests = DictReader(open(utils.givenTestsCSVPathFinal), delimiter = ",")

        for row in dictReaderPeoples:

            vaccines = []

            dictReaderVaccines = DictReader(open(utils.givenVaccineCSVPathFinal), delimiter = ",")

            for givenVaccinesRow in dictReaderVaccines:
                if givenVaccinesRow['PersonID'] == row['id']:
                    certificateOfVaccination = {
                        'QRCode':                       self.__handleEmptyString(
                                givenVaccinesRow['Certification QR Code']),
                        'diseaseOrAgentTargeted':       self.__handleIntParsing(
                                givenVaccinesRow['Disease or Agent Targeted']),
                        'vaccineOrProphylaxis':         self.__handleIntParsing(
                                givenVaccinesRow['Vaccine or Prophylaxis']),
                        'vaccineProduct':               self.__handleEmptyString(givenVaccinesRow['Vaccine Product']),
                        'uniqueCertificateIdentifier':  self.__handleEmptyString(
                                givenVaccinesRow['Unique Certificate Identifier']),
                        'doseNumber':                   self.__handleIntParsing(givenVaccinesRow['DoseNumber']),
                        'totalSeriesOfDoses':           self.__handleIntParsing(
                                givenVaccinesRow['Total Series of Doses']),
                        'countryOfVaccination':         self.__handleEmptyString(
                                givenVaccinesRow['Country of Vaccination']),
                        'marketingAuthorizationHolder': self.__handleEmptyString(
                                givenVaccinesRow['Marketing Authorization Holder']),
                        'certificateIssuer':            self.__handleEmptyString(
                                givenVaccinesRow['Certificate Issuer']),
                        'certificateValidFrom':         self.__handleDateParsing(
                                givenVaccinesRow['Certificate valid from']),
                        'certificateValidUntil':        self.__handleDateParsing(
                                givenVaccinesRow['Certificate valid until']),
                        'schemaVersion':                self.__handleEmptyString(givenVaccinesRow['Schema version'])
                    }

                    vaccine = {

                        'date':                     self.__handleDateParsing(givenVaccinesRow['VaccinationDate']),
                        'healthServiceID':          self.__createDBRef(collectionName = "healthcareService",
                                                                       objectId = utils.getHexString(
                                                                               text = self.__handleEmptyString(
                                                                                       givenVaccinesRow[
                                                                                           'HealthServiceID']),
                                                                               lenght = 24), db = db),

                        'hubID':                    utils.getHexString(
                                self.__handleEmptyString(givenVaccinesRow['HubID']), 24),
                        'lotID':                    self.__createDBRef(collectionName = "vaccineLot",
                                                                       objectId = self.__handleEmptyString(
                                                                               givenVaccinesRow['LotID']), db = db),
                        'healthWorkerPersonalID':   self.__createDBRef(collectionName = "person",
                                                                       objectId = utils.getHexString(
                                                                               text = self.__handleEmptyString(
                                                                                       row['id']), lenght = 24),
                                                                       db = db),
                        'certificateOfVaccination': certificateOfVaccination
                    }

                    vaccines.append(vaccine)

            tests = []

            dictReaderTests = DictReader(open(utils.givenTestsCSVPathFinal), delimiter = ",")

            for givenTestsRow in dictReaderTests:
                if givenTestsRow['PersonID'] == row['id']:
                    certificateOfTesting = {

                        'QRCode':                      self.__handleEmptyString(givenTestsRow['Certification QR Code']),
                        'diseaseOrAgentTargeted':      self.__handleIntParsing(
                                givenTestsRow['Disease or Agent Targeted']),
                        'testType':                    self.__handleEmptyString(givenTestsRow['Test Type']),
                        'resultOfTheTest':             self.__handleIntParsing(givenTestsRow['Result of the Test']),
                        'uniqueCertificateIdentifier': self.__handleEmptyString(
                                givenTestsRow['Unique Certificate Identifier']),
                        'countryOfTesting':            self.__handleEmptyString(givenTestsRow['Country of Testing']),
                        'certificateIssuer':           'Italian Ministry of Health',
                        'certificateValidFrom':        self.__handleDateParsing(
                                givenTestsRow['Certificate valid from']),
                        'certificateValidUntil':       self.__handleDateParsing(
                                givenTestsRow['Certificate valid until']),
                        'schemaVersion':               self.__handleEmptyString(givenTestsRow['Schema version'])

                    }

                    test = {
                        'type':                   self.__handleEmptyString(givenTestsRow['Type']),
                        'date':                   self.__handleDateParsing(givenTestsRow['Test Date']),
                        'healthcareServiceID':    self.__createDBRef(collectionName = "healthcareService",
                                                                     objectId = utils.getHexString(
                                                                             text = self.__handleEmptyString(
                                                                                     givenTestsRow['HealthServiceID']),
                                                                             lenght = 24), db = db),
                        'hubID':                  utils.getHexString(self.__handleEmptyString(givenTestsRow['HubID']),
                                                                     24),
                        'healthWorkerPersonalID': self.__createDBRef(collectionName = "person",
                                                                     objectId = utils.getHexString(
                                                                             self.__handleEmptyString(
                                                                                     row['id']), lenght = 24), db = db),
                        'isPositive':             ast.literal_eval(self.__handleEmptyString(givenTestsRow['Positive'])),
                        'certificateOfTesting':   certificateOfTesting
                    }

                    tests.append(test)

            personalInformation = {'firstName':   self.__handleEmptyString(row['name']),
                                   'lastName':    self.__handleEmptyString(row['surname']),
                                   'fullName':    self.__handleEmptyString(row['fullname']),
                                   'birthDate':   self.__handleDateParsing(row['birth date']),
                                   'sex':         self.__handleEmptyString(row['sex']),
                                   'phoneNumber': self.__handleIntParsing(row['phone_number']),
                                   'address':     self.__handleEmptyString(row['address']),
                                   'city':        self.__handleEmptyString(row['city']),
                                   'state':       self.__handleEmptyString(row['state'])}

            emergencyContact = {'phoneNumber':        self.__handleIntParsing(row['emergency_phone_number']),
                                'parentRelationship': self.__handleEmptyString(row['emergency_parent_relationship']),
                                'personID':           self.__createDBRef(collectionName = "person",
                                                                         objectId = utils.getHexString(
                                                                                 text = self.__handleEmptyString(
                                                                                         row['emergency_person_id']),
                                                                                 lenght = 24), db = db),
                                }

            personDoc = {

                '_id':                             ObjectId(
                        utils.getHexString(text = self.__handleEmptyString(row['id']), lenght = 24)),
                'personalRecognitionDocumentID':   self.__handleEmptyString(row['id']),
                'personalRecognitionDocumentType': self.__handleEmptyString(row['id_type']),
                'personalInformation':             personalInformation,
                'role':                            self.__handleEmptyString(row['role']),
                'healthcareServiceID':             self.__handleEmptyString(row['healthServiceID']),
                'emergencyContact':                emergencyContact,
                'vaccines':                        vaccines,
                'tests':                           tests}

            personCollection.insert_one(document = personDoc)

    def __createVaccineLotDocuments(self, db) -> None:

        vaccineLotCollection = db['vaccineLot']

        dictReaderLots = DictReader(open(utils.vaccineLotsCSVPathFinal), delimiter = ",")

        for row in dictReaderLots:
            vaccineLotDoc = {

                '_id':            ObjectId(self.__handleEmptyString(row['LotID'])),
                'manufacturer':   self.__handleEmptyString(row['Manufacturer']),
                'type':           self.__handleEmptyString(row['Type']),
                'name':           self.__handleEmptyString(row['Name']),
                'productionDate': self.__handleDateParsing(row['Production Date']),
                'expirationDate': self.__handleDateParsing(row['Expiration Date'])
            }

            vaccineLotCollection.insert_one(document = vaccineLotDoc)

    def __getHubDictFomServiceID(self, serviceID, hubCsvPath: str) -> list[dict]:
        dictReaderHub = DictReader(open(hubCsvPath), delimiter = ",")

        dicts = []
        for row in dictReaderHub:
            if row['healtcareServiceID'] == serviceID:
                entry = {

                    '_id':         ObjectId(
                            utils.getHexString(text = self.__handleEmptyString(row['ID']), lenght = 24)),
                    'name':        self.__handleEmptyString(row['Name']),
                    'type':        self.__handleEmptyString(row['Type']),
                    'coordinates': utils.getGeoJsonPoint(
                            longitude = self.__handleFloatParsing(row['Longitude']),
                            latitude = self.__handleFloatParsing(row['Latitude'])),
                    'address':     self.__handleEmptyString(row['Address']),
                    'cap':         self.__handleIntParsing(row['CAP']),
                    'city':        self.__handleEmptyString(row['City']),
                    'region':      self.__handleEmptyString(row['Region']),
                    'regionCode':  self.__handleIntParsing(row['Region Code']),
                    'state':       self.__handleEmptyString(row['State'])
                }

                dicts.append(entry)

        return dicts

    def __createHealthcareServiceDocuments(self, db) -> None:

        healthcareServiceCollection = db['healthcareService']
        dictReaderServices = DictReader(open(utils.healthcareServicesCSVPathFinal), delimiter = ",")

        for row in dictReaderServices:
            vaccineHubs = self.__getHubDictFomServiceID(serviceID = row['ID'],
                                                        hubCsvPath = utils.vaccineHubsCSVPathFinal)
            testHubs = self.__getHubDictFomServiceID(serviceID = row['ID'], hubCsvPath = utils.testHubsCSVPathFinal)

            healthService = {
                '_id':         ObjectId(utils.getHexString(text = self.__handleEmptyString(row['ID']), lenght = 24)),
                'name':        self.__handleEmptyString(row['Name']),
                'type':        self.__handleEmptyString(row['Type']),
                'address':     self.__handleEmptyString(row['Address']),
                'cap':         self.__handleIntParsing(row['CAP']),
                'city':        self.__handleEmptyString(row['City']),
                'region':      self.__handleEmptyString(row['Region']),
                'regionCode':  self.__handleIntParsing(row['Region Code']),
                'state':       self.__handleEmptyString(row['State']),
                'coordinates': utils.getGeoJsonPoint(
                        longitude = self.__handleFloatParsing(row['Longitude']),
                        latitude = self.__handleFloatParsing(row['Latitude'])),
                'vaccineHubs': vaccineHubs,
                'testHubs':    testHubs

            }

            healthcareServiceCollection.insert_one(document = healthService)

    def populateDatabase(self, databaseName: str) -> None:

        database = self[databaseName]
        self.__createPersonDocuments(db = database)
        self.__createVaccineLotDocuments(db = database)
        self.__createHealthcareServiceDocuments(db = database)


# Execute this Main to populate the database
if __name__ == '__main__':
    uri = "MONGODB_URI"
    mongoDB = MongoDB(connectionURI = uri)
    mongoDB.populateDatabase(databaseName = 'DATABASE_NAME')
