import socket
import struct
from obspy import Trace, read, Stream
    
MCAST_GRP = '234.0.0.1'
MCAST_PORT = 7001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                             # to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# while True:
# Получили с сокета данные
data=sock.recv(512)
print(data)

# Записали данные в файл
f = open('test.mseed','wb+')
f.write(data)
f.close()

# Прочитали с файла
read('test.mseed')
# Но получили ошибку формата

