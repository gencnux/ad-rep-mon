# Python shell'inde çalıştırın
from ldap3 import Server, Connection, ALL
server = Server('172.25.217.37', get_info=ALL)
conn = Connection(server, user="t0.rkensa@adom.local", password="Pssw0rd", authentication='NTLM')
conn.bind()
conn.search('CN=Sites,CN=Configuration,DC=adom,DC=local', '(objectClass=nTDSConnection)', attributes=['*'])
print("Entries:", conn.entries)