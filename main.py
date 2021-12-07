from pymongo import MongoClient

uri = "mongodb+srv://root:SMBUD2021@smbud.li4eh.mongodb.net/SMBUD"

client = MongoClient(uri)

# to see connection status
print(str(client.stats))
# print(str(client.list_database_names()))

smbudDb = client['SMBUD']


def createPersonDocument(db) -> None:
    personDoc = db['person']




