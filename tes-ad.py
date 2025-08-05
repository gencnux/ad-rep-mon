import ldap3

server = ldap3.Server('172.25.217.37', port=389)
conn = ldap3.Connection(server, 
                       user='adom\\t0.rkensa', 
                       password='Pssw0rd',
                       raise_exceptions=True)
try:
    conn.bind()
except Exception as e:
    print("Hata detayı:", e)