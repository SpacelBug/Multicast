import socket
from struct import unpack, pack
from obspy import Trace, read, Stream
    
MCAST_GRP = '234.0.0.1'
MCAST_PORT = 7001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                             # to MCAST_GRP, not all groups on MCAST_PORT
mreq = pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

#while True:

x=sock.recv(512)
print(x)

# Распаковка первых 48 байт и blockette`ов
flag=0
fixedHeader=['']
# Порядковый номер распакован не верно
for i in unpack('>6B2c5s2s3s2s2H4B2H2h4Bi2H', x[0:48]):
    if (flag < 6):
        fixedHeader[0]=fixedHeader[0]+str(i)
        flag=flag+1
    else:
        fixedHeader.append(i)

blockette_1000=[]
for i in unpack('>2H4B',x[48:56]):
    blockette_1000.append(i)

blockette_1001=[]
for i in unpack('>2HBb2B',x[56:64]):
    blockette_1001.append(i)
