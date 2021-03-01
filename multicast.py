import socket
import struct
import os
from threading import Thread
import io
from obspy import read

def formMSEED(name):
	while True:
		# Получили с сокета данные
		data=sock.recv(512)
		# Берем порядковый номер и форматируем его к виду ######
		# Пока не знаю верно ли он взят, но он нужен для того,
		# Чтобы привести наши данные к читаемому формату.
		SqenNum = '{:0>6}'.format(str(int.from_bytes(data[4:6],'big')))
		# Меняем первые шесть байт и перезаписываем дату в нормальный формат
		data = (read(io.BytesIO(SqenNum.encode()+data[6:]), format='MSEED'))
		# Если имен совпадают то переходим к записи
		if (name==data[0].stats.station+' '+data[0].stats.location+data[0].stats.channel+data[0].stats.network):
			# Проверяем существует ли файл
			if os.path.exists('seeds/'+name+'.mseed'):
				# Суммируем stream`ы (тот что постумил из мультикаста
				# с тем что уже был записан в соответствующем файле)
				oldData = read('seeds/'+name+'.mseed')
				newData = oldData + data
				newData.write('seeds/'+name+'.mseed')
			else:
				# Просто записываем stream в файл
				data.write('seeds/'+name+'.mseed')

# Всякое разное для мультикаста
MCAST_GRP = '234.0.0.1'
MCAST_PORT = 7001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                             # to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Список наблюдаемых станций
station_list = ['BKI 02SHNYY','BZM 02SHEYY','GRL 02SHEYY']

# Выделяем каждой станции свой поток
for name in station_list:
	Thread(target=formMSEED, args=(name,)).start()

