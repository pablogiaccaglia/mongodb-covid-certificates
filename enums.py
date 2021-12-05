import utils
from enum import Enum


class VaccineManufacturer(Enum):
    PFIZER = "PFIZER",
    MODERNA = "MODERNA",
    JOHNSON_JOHNSON = "JOHNSON&JOHNSON",
    ASTRAZENECA = "ASTRAENECA"


class VaccineLotNumber(Enum):
    PFIZER = utils.getRandomPfizerLotNumber,
    MODERNA = utils.getRandomModernaLotNumber,
    JOHNSON_JOHNSON = utils.getRandomJJLotNumber
    ASTRAZENECA = utils.getRandomAstrazenecaLotNumber


class VaccineVialNumber(Enum):
    PFIZER = utils.getRandomPfizerVialNumber,
    MODERNA = utils.getRandomModernaVialNumber,
    JOHNSON_JOHNSON = utils.getRandomJJVialNumber
    ASTRAZENECA = utils.getRandomAstrazenecaVialNumber


class TelephoneCompanyAreaCode(Enum):
    ILIAD_ITALIA = [3513, 3514, 3515, 3516, 3517, 3518, 3519, 3520],
    TIM = [330, 331, 333, 334, 335, 336, 337, 338, 339, 360, 361, 362, 363, 366, 368, 381],
    VODAFONE_ITALIA = [340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 383],
    WIND_TRE = [320, 322, 323, 324, 327, 328, 329, 355, 380, 388, 389, 390, 391, 392, 393, 397],
    UNO_MOBILE = [3773, 3793],
    BT_MOBILE = [3710, 3777],
    COOP_VOCE = [3311, 3703, 3534],
    DAILY_TELECOM_MOBILE = [3778],
    FASTWEB = [373, 3755, 3756, 3757],
    HO_MOBILE = [3770, 3791, 3792],
    KENA_MOBILE = [3500, 3501, 3505],
    LYCAMOBILE = [3509, 3510, 3511, 3512, 373, 382],
    POSTEMOBILE = [3711, 371 - 3, 371 - 4, 371 - 5, 377 - 2, 377 - 4, 377 - 6, 377 - 9],
    TISCALI_MOBILE = [3701],
    WELCOME_ITALIA = [3783],
    VERYMOBILE = [320]
