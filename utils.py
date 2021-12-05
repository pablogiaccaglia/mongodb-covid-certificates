import random
import string
from enum import Enum
import datetime
import random
import string
from collections import namedtuple
from csv import DictReader, DictWriter, reader, writer
from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim
import pandas as pd
from enums import *

""" paths of CSV files in the 'final' folder """
italianHospitalsCSVPath = 'datasets/final/italian_hospitals_standardized_no_nulls_no_duplicates_with_streets.csv'
italianCitiesCSVPath = 'datasets/final/italy_cities.csv'
italianStreetsCSVPath = 'datasets/final/italian_streets_no_duplicates_standardized.csv'
vaccinesCSVPath = 'datasets/final/italian_vaccines.csv'
peopleCSVPath = 'datasets/final/people.csv'
covidTestsCSVPath = 'datasets/final/covid_tests.csv'


def generateRandomString(length: int) -> str:
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


def generateRandomNumber(length: int) -> int:
    rangeStart = 10 ** (length - 1)
    rangeEnd = (10 ** length) - 1
    return random.randint(rangeStart, rangeEnd)


def getRandomPfizerLotNumber() -> str:
    """ Generates a Random Pfizer lot number,
        whose structure is 2 letters + 4 digits.

        Example: EL9269"""

    return generateRandomString(2) + str(generateRandomNumber(4))

    pass


def getRandomModernaLotNumber() -> str:
    """ Generates a Random Moderna lot number,
        whose structure is 3 digit + 1 letter + 2 digits + 1 letter.

        Example: 027L20A"""

    return str(generateRandomNumber(3)) + generateRandomString(1) + \
           str(generateRandomNumber(2)) + generateRandomString(1)
    pass


def getRandomJJLotNumber() -> str:
    """ Generates a Random Johnson & Johnson lot number,
        which is composed by 7 digits.

        Example: 1805031"""

    return str(generateRandomNumber(7))

    pass


def getRandomAstrazenecaLotNumber() -> str:
    """ Generates a Random Astrazeneca lot number,
        whose structure is 3 letters + 4 digits.

        Example: ABV3746"""

    return generateRandomString(3) + str(generateRandomNumber(4))

    pass


def getRandomPfizerVialNumber(lotNumber: str) -> str:
    """ Generates a Random Pfizer lot number,
        whose (fictional) structure is LotNumber + 4 digits.

        Example: EL92695521"""

    return lotNumber + str(generateRandomNumber(4))

    pass


def getRandomModernaVialNumber(lotNumber: str) -> str:
    """ Generates a Random Moderna lot number,
        whose (fictional) structure is LotNumber + 4 digits.

        Example: 027L20A9555"""

    return lotNumber + str(generateRandomNumber(4))

    pass


def getRandomJJVialNumber(lotNumber: str) -> str:
    """ Generates a Random Johnson & Johnson lot number,
        whose (fictional) structure is LotNumber + 4 digits.

        Example: 18050312308"""

    return lotNumber + str(generateRandomNumber(4))

    pass


def getRandomAstrazenecaVialNumber(lotNumber: str) -> str:
    """ Generates a Random Astrazeneca lot number,
        whose (fictional) structure is LotNumber + 4 digits.

        Example: ABV37467622"""

    return lotNumber + str(generateRandomNumber(4))

    pass


def generateRandomHealthcareWorkerID() -> str:
    """ Generates a Random Italian Healthcare Worker identification number,
        whose (fictional) structure is 2 letters - 7 digits - 4 letters"""

    HealthcareWorkerID = \
        generateRandomString(2) + \
        str(random.randrange(1000, 10000)) + \
        generateRandomString(4)

    return HealthcareWorkerID


# TODO
def addGPSToLocationsCSV(csvPath, delimiter) -> None:
    pass


# TODO
def addOpeningAndClosingDateToHUBCSV(csvPath, delimiter) -> None:
    pass


# TODO
def getRandomParentRelationship() -> str:
    pass


def getRandomPhoneNumber() -> str:
    """Generates a Random Italian mobile phone number,
        whose (fictional) structure is area code (4 digits) + telephone company area code (3/4 digits) + 7/6 digits """

    areaCode = "0039"
    telephoneCompanyAreaCode = str(random.choice(random.choice(list(TelephoneCompanyAreaCode)).value))
    length = 7 if len(telephoneCompanyAreaCode) == 3 else 6

    return areaCode + telephoneCompanyAreaCode + str(generateRandomNumber(length = length))


def getRandomLotNumber(manufacturer: VaccineManufacturer):
    return VaccineLotNumber[manufacturer].value()


def getRandomVialNumber(manufacturer: VaccineManufacturer, lotNumber: str):
    return VaccineVialNumber[manufacturer].value(lotNumber = lotNumber)


# TODO
def getRandomCertificationID() -> str:
    pass


def getRandomItalianAddress() -> str:
    """ Picks a random Italian street address (name + number) from the CSV 'italian_streets_no_duplicates_standardized.
        Example : 'Via Certaldese 155' """

    csvFile = pd.read_csv(italianStreetsCSVPath)
    sample = csvFile.sample()
    address = sample.values[0][0]
    return address


def calculateAge(born: datetime) -> int:
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def parseDate(date: str) -> datetime:
    return datetime.datetime.strptime(date, '%Y-%m-%d')


def getRandomPersonID() -> str:
    """ Picks a random person's ID from the CSV 'people'.
        The ID belongs to a person node in the database """

    csvFile = pd.read_csv(peopleCSVPath)
    sample = csvFile.sample()
    personID = sample.values[0][5]
    return personID


partialPersonInfo = namedtuple("PartialPersonInfo", ['id', 'sex', 'age'])


def getRandomPersonPartialInfo() -> partialPersonInfo:
    """ Picks a random person's partial information (id, sex, age) from the CSV 'people'"""

    csvFile = pd.read_csv(peopleCSVPath)
    sample = csvFile.sample()
    personID = sample.values[0][5]
    personSex = sample.values[0][3]
    personAge = int(calculateAge(parseDate(sample.values[0][4])))

    return partialPersonInfo(id = personID, sex = personSex, age = personAge)

def getOppositeSex(sex : str) -> str:

    if sex == "male":
        return "female"
    if sex == "female":
        return "male"