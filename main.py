from pymongo import MongoClient

uri = "mongodb+srv://root:SMBUD2021@smbud.li4eh.mongodb.net/SMBUD"

client = MongoClient(uri)

# to see connection status
print(str(client.stats))
# print(str(client.list_database_names()))

smbud = client['SMBUD']
print(str(smbud.list_collection_names()))
