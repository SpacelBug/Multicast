import socket, os, struct, io
from threading import Thread
from obspy import read

class mseedFromMulticast:
	# Инициализация
	def __init__ (self):
		self.MCAST_GRP = '234.0.0.1'
		self.MCAST_PORT = 7001
		self.station_list = ['BKI 02SHNYY','BZM 02SHEYY','GRL 02SHEYY']
		self.sock = socket
		self.multicastConnection()
	# Формирование Mseed`ов 
	def formMseed (self, name):
			while True:
				# Получили с сокета данные
				data=self.sock.recv(512)
				print(os.getpid())
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
	# Подключение на мультикаст
	def multicastConnection (self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', self.MCAST_PORT)) # use MCAST_GRP instead of '' to listen only
                             		# to MCAST_GRP, not all groups on MCAST_PORT
		self.mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)

		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
	# Распаточить формирование Mseed`ов 
	def multiTreading (self):
		for name in self.station_list:
			Thread(target=self.formMseed, args=(name,)).start()

# Создаем класс и запускаем его метод
multiMseed = mseedFromMulticast()
multiMseed.multiTreading()
