import base64
import zlib
from enum import Enum
import datetime
import random
import string
from functools import partial
from typing import Any
from geojson import Point
import base45
import pandas as pd
import qrcodeutils

import json
import googlemaps
from collections import namedtuple

""" paths of CSV files in the 'final' folder """
italianHospitalsCSVPath = 'datasets/final/italian_hospitals_standardized_no_nulls_no_duplicates_with_streets.csv'
italianCitiesCSVPath = 'datasets/original/italy_cities.csv'
italianStreetsCSVPath = 'datasets/original/italian_streets_no_duplicates_standardized.csv'
vaccinesCSVPath = 'datasets/final/italian_vaccines.csv'
peopleCSVPath = 'datasets/original/people.csv'
peopleCSVPathWithPhoneNumbers = 'datasets/original/people_with_phone_numbers.csv'
peopleCSVPathFinal = 'datasets/final/people_with_phone_numbers_with_address_info_with_healtcare_info_with_emergency_contact_info.csv'
covidTestsCSVPath = 'datasets/final/covid_tests.csv'
vaccineLotsCSVPath = 'datasets/original/covid_vaccine_lots.csv'
vaccineHub_HealthServiceMappingCSVPath = 'datasets/final/vaccineHubs-services id mapping.csv'
testHub_HealthServiceMappingCSVPath = 'datasets/final/TestHubs-services id mapping.csv'
givenVaccineCSVPathFinal = 'datasets/final/given_vaccines_with_encoded_qr.csv'
givenTestsCSVPathFinal = 'datasets/final/given_tests_with_encoded_qr.csv'
vaccineLotsCSVPathFinal = 'datasets/final/covid_vaccine_lots_standardized.csv'
healthcareServicesCSVPathFinal = 'datasets/final/asl italia 3_converted_standardized_no_duplicates_with_service_type_with_ID_with_coordinates.csv'
vaccineHubsCSVPathFinal = 'datasets/final/punti-somministrazione-tipologia_standardized_no_duplicates_with_ID_with_location_info_with_service_id.csv'
testHubsCSVPathFinal = 'datasets/final/italian pharmacies_converted_no_duplicates_with_ID_no_nulls_standardized_with_service_id.csv'

ProductionAndExpirationDates = namedtuple("ProductionAndExpirationDates", ['productionDate', 'expirationDate'])
partialPersonInfo = namedtuple("PartialPersonInfo", ['id', 'sex', 'age', 'phoneNumber'])
CityInfoTuple = namedtuple("CityInfoTuple", ["name", "ID", "country"])
Hub_ServiceMappingTuple = namedtuple("Hub_ServiceMapping", ['HealthcareServiceID', 'HubID'])
Location = namedtuple("Location",
                      ["route", "streetNumber", "city", "postalCode", "longitude", "latitude", "formattedAddress"])

gmapsClient = googlemaps.Client(key = 'API_KEY')


def generateRandomHexString(lenght: int) -> str:
    lst = [random.choice(string.hexdigits) for n in range(lenght)]
    s = "".join(lst)
    return s


def getRandomDate(start_date = datetime.date(2020, 11, 1), end_date = datetime.date(2021, 10, 1)) -> datetime:
    """ Generates a random datetime in between the start_date and the end_date.
        In case of one or both missing parameters, the default values are used """

    start_date = start_date
    end_date = end_date

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days = random_number_of_days)

    return random_date


def generateRandomString(length: int) -> str:
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


def generateRandomStringWithNumbers(length: int) -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def generateRandomNumber(length: int) -> int:
    rangeStart = 10 ** (length - 1)
    rangeEnd = (10 ** length) - 1
    return random.randint(rangeStart, rangeEnd)


def getRandomPfizerLotNumber() -> str:
    """ Generates a Random Pfizer lot number,
        whose structure is 24 chars.

        Example: EL9269"""

    return generateRandomHexString(12) + str(generateRandomNumber(12))

    pass


def getRandomModernaLotNumber() -> str:
    """ Generates a Random Moderna lot number,
        whose structure is is 24 chars.

        Example: 027L20A"""

    return str(generateRandomNumber(6)) + generateRandomHexString(6) + \
           str(generateRandomNumber(6)) + generateRandomHexString(6)
    pass


def getRandomJJLotNumber() -> str:
    """ Generates a Random Johnson & Johnson lot number,
        which is composed by 24 chars.

        Example: 1805031"""

    return str(generateRandomNumber(7)) + generateRandomHexString(17)

    pass


def getRandomAstrazenecaLotNumber() -> str:
    """ Generates a Random Astrazeneca lot number,
        whose structure is 24 CHARS

        Example: ABV3746"""

    return generateRandomHexString(10) + str(generateRandomNumber(14))

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

def getRandomPhoneNumber() -> str:
    """Generates a Random Italian mobile phone number,
        whose (fictional) structure is area code (4 digits) + telephone company area code (3/4 digits) + 7/6 digits """

    areaCode = "0039"
    telephoneCompanyAreaCode = str(random.choice(random.choice(list(TelephoneCompanyAreaCode)).value))
    length = 7 if len(telephoneCompanyAreaCode) == 3 else 6

    return areaCode + telephoneCompanyAreaCode + str(generateRandomNumber(length = length))


def getRandomItalianAddress() -> str:
    """ Picks a random Italian street address (name + number) from the CSV 'italian_streets_no_duplicates_standardized.
        Example : 'Via Certaldese 155' """

    csvFile = pd.read_csv(italianStreetsCSVPath)
    sample = csvFile.sample()
    address = sample.values[0][0]
    return address


def getRandomItalianCityInfo() -> CityInfoTuple:
    """ Picks a random Italian city information (name + id + country) from the CSV 'italy_cities.csv'.
            Example : 'Milan,1380724377,ITA' """

    csvFile = pd.read_csv(italianCitiesCSVPath)
    sample = csvFile.sample()
    name = sample.values[0][0]
    ID = sample.values[0][5]
    country = sample.values[0][2]

    return CityInfoTuple(name = name, ID = ID, country = country)


def getRandomHub_ServiceMapping(csvFilePath: str) -> Hub_ServiceMappingTuple:
    csvFile = pd.read_csv(csvFilePath)
    sample = csvFile.sample()
    healthcareServiceID = sample.values[0][0]
    hubID = sample.values[0][1]

    return Hub_ServiceMappingTuple(HealthcareServiceID = healthcareServiceID, HubID = hubID)


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


def getRandomPersonPartialInfo() -> partialPersonInfo:
    """ Picks a random person's partial information (id, sex, age, phone number) from the CSV 'people'"""

    csvFile = pd.read_csv(peopleCSVPathWithPhoneNumbers)
    sample = csvFile.sample(n = 1)
    personID = sample.values[0][5]
    personSex = sample.values[0][3]
    personAge = int(calculateAge(parseDate(sample.values[0][4])))
    phoneNumber = int(sample.values[0][7])

    return partialPersonInfo(id = personID, sex = personSex, age = personAge, phoneNumber = phoneNumber)


class VaccineManufacturer(Enum):
    PFIZER = "PFIZER"
    MODERNA = "MODERNA"
    JOHNSON_JOHNSON = "JOHNSON&JOHNSON"
    ASTRAZENECA = "ASTRAZENECA"


class VaccineBrandName(Enum):
    PFIZER = "COMIRNATY"
    MODERNA = "mRNA-1273"
    JOHNSON_JOHNSON = "JNJ-78436735"
    ASTRAZENECA = "VAXZEVRIA"


class VaccineLotNumber(Enum):
    PFIZER = partial(getRandomPfizerLotNumber)
    MODERNA = partial(getRandomModernaLotNumber)
    JOHNSON_JOHNSON = partial(getRandomJJLotNumber)
    ASTRAZENECA = partial(getRandomAstrazenecaLotNumber)


class VaccineVialNumber(Enum):
    PFIZER = partial(getRandomPfizerLotNumber)
    MODERNA = partial(getRandomModernaVialNumber)
    JOHNSON_JOHNSON = partial(getRandomJJVialNumber)
    ASTRAZENECA = partial(getRandomAstrazenecaVialNumber)


class VaccineType(Enum):
    PFIZER = "mRNA"
    MODERNA = "mRNA"
    JOHNSON_JOHNSON = "Viral Vector"
    ASTRAZENECA = "Viral vector"


class VaccineProductCode(Enum):
    PFIZER = "EU/1/20/1528"
    MODERNA = "EU/1/20/1507"
    JOHNSON_JOHNSON = "EU/1/20/1525"
    ASTRAZENECA = "EU/1/21/1529"


class VaccineManufacturerCode(Enum):
    PFIZER = "ORG-100030215"
    MODERNA = "ORG-100031184"
    JOHNSON_JOHNSON = "ORG-100001417"
    ASTRAZENECA = "ORG-100001699"


class VaccineCode(Enum):
    PFIZER = "1119349007"
    MODERNA = "1119349007"
    JOHNSON_JOHNSON = "1119305005"
    ASTRAZENECA = "1119305005"


class CovidTest(Enum):
    MOLECULAR = "Molecular test"
    ANTIGEN = "Antigen test"
    ANTIBODY = "Antibody test"


class CovidTestResult(Enum):
    MOLECULAR = {
        "Detected":     260373001,
        "Not Detected": 260415000,
    }

    ANTIGEN = {
        "Detected":     260373001,
        "Not Detected": 260415000,
    }

    ANTIBODY = {
        "Detected":     260373001,
        "Not Detected": 260415000,
    }


class CovidTestType(Enum):
    MOLECULAR = "94309-2"
    ANTIGEN = "94558-4"
    ANTIBODY = "94762-2"


class CovidTestResultWaitDays(Enum):
    MOLECULAR = 2
    ANTIGEN = 0
    ANTIBODY = 3


class CovidTestCertificateValidityDays(Enum):
    MOLECULAR = 3
    ANTIGEN = 2
    ANTIBODY = 3


class TelephoneCompanyAreaCode(Enum):
    ILIAD_ITALIA = [3513, 3514, 3515, 3516, 3517, 3518, 3519, 3520]
    TIM = [330, 331, 333, 334, 335, 336, 337, 338, 339, 360, 361, 362, 363, 366, 368, 381]
    VODAFONE_ITALIA = [340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 383]
    WIND_TRE = [320, 322, 323, 324, 327, 328, 329, 355, 380, 388, 389, 390, 391, 392, 393, 397]
    UNO_MOBILE = [3773, 3793]
    BT_MOBILE = [3710, 3777]
    COOP_VOCE = [3311, 3703, 3534]
    DAILY_TELECOM_MOBILE = [3778]
    FASTWEB = [373, 3755, 3756, 3757]
    HO_MOBILE = [3770, 3791, 3792]
    KENA_MOBILE = [3500, 3501, 3505]
    LYCAMOBILE = [3509, 3510, 3511, 3512, 373, 382]
    POSTEMOBILE = [3711, 3713, 3714, 3715, 3772, 3774, 3776, 3779]
    TISCALI_MOBILE = [3701]
    WELCOME_ITALIA = [3783]
    VERYMOBILE = [320]


def getRandomCovidTest() -> CovidTest:
    """ Picks a random Covid test from the CSV 'covid_tests'
        The random choice is among:
        -> Molecular test
        -> Antigen test
        -> Antibody test """

    return random.choice(list(CovidTest))


def getRandomManufacturer() -> VaccineManufacturer:
    return random.choice(list(VaccineManufacturer))


def getCovidTestResultCode(covidTest: CovidTest, isPositive: bool) -> int:
    key = "Detected" if isPositive else "Not Detected"
    return CovidTestResult[covidTest.name].value[key]


def getCovidTestType(covidTest: CovidTest) -> str:
    return CovidTestType[covidTest.name].value


def getCovidTestCertificateValidityDays(covidTest: CovidTest) -> int:
    return CovidTestCertificateValidityDays[covidTest.name].value


def getCovidTestResultWaitDays(covidTest: CovidTest) -> int:
    return CovidTestResultWaitDays[covidTest.name].value


def getVaccineName(manufacturer: VaccineManufacturer) -> VaccineBrandName:
    return VaccineBrandName[manufacturer.name].value


def getRandomLotNumber(manufacturer: VaccineManufacturer):
    return VaccineLotNumber[manufacturer.name].value()


def getVaccineType(manufacturer: VaccineManufacturer) -> VaccineType:
    return VaccineType[manufacturer.name].value


def getRandomVialNumber(manufacturer: VaccineManufacturer, lotNumber: str):
    return VaccineVialNumber[manufacturer.name].value(lotNumber = lotNumber)


def getVaccineProductCode(manufacturer: VaccineManufacturer) -> str:
    return VaccineProductCode[manufacturer.name].value


def getVaccineCode(manufacturer: VaccineManufacturer) -> str:
    return VaccineCode[manufacturer.name].value


def getVaccineManufacturerCode(manufacturer: VaccineManufacturer) -> str:
    return VaccineManufacturerCode[manufacturer.name].value


def getProductionAndExpirationDates() -> ProductionAndExpirationDates:
    productionDate = getRandomDate()
    expirationDate = productionDate + datetime.timedelta(days = random.randint(135, 180))

    return ProductionAndExpirationDates(productionDate = productionDate, expirationDate = expirationDate)


def getRandomUniqueCertificateIdentifier() -> str:
    return "01IT" + generateRandomStringWithNumbers(length = 32) + "#" + str(generateRandomNumber(1))


def encodeAndCompress(encoder, text: str) -> bytes:
    textBytes = text.encode()
    base45Text = encoder(textBytes)

    compressedText = zlib.compress(base45Text)
    return compressedText


def generateQRCodeText(text: str) -> str:
    qrcodeImage = qrcodeutils.textToQRCode(text = text)

    bytesImage = qrcodeutils.imageToBytesArray(image = qrcodeImage)
    decoded = bytesImage

    return base64.b64encode(decoded).decode()


def generateQRCodeBytes(byt: bytes) -> bytes:
    qrcodeImage = qrcodeutils.bytesToQRCode(byt = byt)

    bytesImage = qrcodeutils.imageToBytesArray(image = qrcodeImage)

    return bytesImage


def generateQRCode(text: str) -> str:
    encoded = encodeAndCompress(encoder = base45.b45encode, text = text)
    encodedQRCode = generateQRCodeBytes(byt = encoded)
    return str(base64.b64encode(encodedQRCode))[2:-1]


def getLocationInfo(gmaps: googlemaps.Client, location: str) -> Location:
    # Geocoding an address
    geocode_result = gmaps.geocode(location)

    parsed = json.loads(json.dumps(geocode_result[0]))

    # print(json.dumps(parsed, indent=4, sort_keys=True))

    addressComponents = parsed['address_components']

    streetNumber = None
    route = None
    city = None
    postalCode = None

    for component in addressComponents:
        if "street_number" in component['types']:
            streetNumber = component['long_name']

        if "route" in component['types']:
            route = component['long_name']

        if "locality" in component['types']:
            city = component['long_name']

        if "postal_code" in component['types']:
            postalCode = component['long_name']

    formattedAddress = parsed['formatted_address']

    geometry = parsed['geometry']
    longitude = geometry['location']['lng']
    latitude = geometry['location']['lat']

    if city is None:
        for component in addressComponents:
            if "political" in component['types']:
                city = component['long_name']
                break

    if postalCode is not None:
        postalCode = int(postalCode)

    if longitude is not None:
        longitude = float(longitude)

    if latitude is not None:
        latitude = float(latitude)

    return Location(route = route, streetNumber = streetNumber, city = city, postalCode = postalCode,
                    longitude = longitude, latitude = latitude, formattedAddress = formattedAddress)


def repeatToLength(stringToExpand, length) -> str:
    return (stringToExpand * (int(length / len(stringToExpand)) + 1))[:length]


def getHexString(text: str, lenght: int):
    if text is None:
        return None
    hexRep = str(text.encode('utf-8').hex())
    return repeatToLength(hexRep, lenght)


def getGeoJsonPoint(longitude: float, latitude: float) -> Any:
    if longitude is None or longitude and not isinstance(longitude, float):
        return None

    if latitude is None or latitude and not isinstance(latitude, float):
        return None

    return Point((longitude, latitude))
