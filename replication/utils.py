from ldap3 import Server, Connection, ALL, Tls
from django.conf import settings
import logging
import ssl

logger = logging.getLogger(__name__)

def get_replication_status():
    conn = None
    try:
        # 1. TLS/SSL Ayarları (LDAPS için)
        tls_config = Tls(
            validate=Tls(ssl.CERT_NONE),
            version=ssl.PROTOCOL_TLSv1_2,
            ciphers='DEFAULT:@SECLEVEL=1'  # Test ortamı için güvenlik seviyesini düşür
        )
        
        # 2. Sunucu Bağlantısı
        server = Server(
            settings.AD_SERVER,
            port=636,  # LDAPS portu
            use_ssl=True,
            tls=tls_config,
            get_info=ALL
        )
        
        # 3. Kullanıcı Adı Formatları (Denenecek sırayla)
        user_formats = [
            f"adom\\{settings.AD_USER}",  # NetBIOS formatı
            f"{settings.AD_USER}@adom.local",  # UPN formatı
            settings.AD_USER  # Sadece kullanıcı adı
        ]
        
        # 4. Bağlantı Denemeleri
        for user in user_formats:
            try:
                conn = Connection(
                    server,
                    user=user,
                    password=settings.AD_PASSWORD,
                    authentication='NTLM',
                    auto_referrals=False,
                    receive_timeout=15
                )
                
                if conn.bind():
                    logger.info(f"Successfully connected as {user}")
                    break
                    
            except Exception as e:
                logger.warning(f"Failed with {user}: {str(e)}")
                continue
        else:
            return {'error': 'All authentication attempts failed'}
        
        # 5. Replikasyon Verilerini Sorgula
        search_base = f"CN=Sites,CN=Configuration,{settings.AD_SEARCH_BASE}"
        if not conn.search(
            search_base,
            '(objectClass=nTDSConnection)',
            attributes=['fromServer', 'enabledConnection']
        ):
            return {'error': f"Search failed: {conn.result['description']}"}
        
        # 6. Sonuçları İşle
        results = [{
            'source': str(entry.fromServer.value).split(',')[0].replace('CN=', ''),
            'status': 'Active' if entry.enabledConnection.value else 'Inactive'
        } for entry in conn.entries]
        
        return {'data': results if results else {'info': 'No replication links found'}}
        
    except Exception as e:
        logger.exception("LDAP Error")
        return {'error': f"Connection error: {str(e)}"}
    finally:
        if conn and conn.bound:
            conn.unbind()