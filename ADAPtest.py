from obspy import read
import cmath, time

st=read('seeds/example.msd')

st6=st.copy()
st7=st.copy()
st13=st.copy()
st14=st.copy()
st15=st.copy()

st6=st6.filter('bandpass', freqmin=0.75, freqmax=1.5, corners=4, zerophase=False)
st7=st7.filter('bandpass', freqmin=1, freqmax=2, corners=4, zerophase=False)
st13=st13.filter('bandpass', freqmin=8, freqmax=16, corners=4, zerophase=False)
st14=st14.filter('bandpass', freqmin=12, freqmax=18, corners=4, zerophase=False)
st15=st15.filter('bandpass', freqmin=0.1, freqmax=18, corners=4, zerophase=False)

Hranges=[['SMK','SRK', 'CIR'],[1.333,1.333,1.0]] # Числовые диапазоны для определения выброса
tr_id=0


for tr in st:
	print('\n',tr.stats.station)
	print(tr.stats.starttime,'|',tr.stats.endtime,'\n')
	amp_id=0 # Использую его для того чтобы обращаться к текущей амплитуде

	ampold = 0 # В эту переменную записывается предществующая амплитуда 15-й полосы
	ampold6 = 0 # В эту переменную записывается предществующая амплитуда 6-й полосы
	ampold7 = 0 # В эту переменную записывается предществующая амплитуда 7-й полосы
	I = 0 # Хранит в себе I предыдущей итерации цикла

	for amp in tr.data:
		#print(time.perf_counter())
		#print('*******************************************************************')

		'''*************************************
		Считаем величину I опр. возрастание или 
		затухание сигнала в заданной частотной 
		полосе (15-й)
		*************************************'''

		tr15=st15[tr_id].data[amp_id]
		if ampold!=0:
			i=cmath.log(ampold/tr15).real
		else:
			i=0
		ampold=tr15

		'''***************************
		Фильтруем данные по частотам
		Считаем I для 6-й и 7-й полос

		(Необходимо в проверке наличия
		выброса)
		***************************'''

		tr6=st6[tr_id].data[amp_id]
		if ampold6!=0:
			i6=cmath.log(ampold6/tr6).real
		else:
			i6=0

		tr7=st7[tr_id].data[amp_id]
		if ampold7!=0:
			i7=cmath.log(ampold7/tr7).real
		else:
			i7=0

		ampold6 = tr6
		ampold7 = tr7

		'''************************************
		Теперь находим индекс Fi
		Fi=log10((A13+A14)/(A6+A7))
		Где An - амплитуда в n частотной полосе

		Прим.

		Fi следует искать только в том случает,
		если I 15 резко уходит в отрицательные 
		значения

		Также необходимым условием выброса явл.
		отрицалтельные значения I в 6-й и 7-й
		полосах
		************************************'''

		if (i<-2):
			if ((i6<0)and(i7<0)):
				tr13=st13[tr_id].data[amp_id].real
				tr14=st14[tr_id].data[amp_id].real

				#print('filtred amp: tr13=',tr13,' tr14=',tr14, ' tr6=',tr6 ,' tr7=',tr7 )

				Fi=cmath.log10((tr13+tr14)/(tr6+tr7)).real # Индекс выделения пеплового выброса
				#print('Fi = ',Fi)

				'''**************************************
				Теперь, если Fi лежит в опр для конкретн
				вулкана числовом диапазоне, то можно 
				вычислять высоту пеплового выброса

				H=KFiAn(I-1)
				An - амплитуда сейсм. сигнала по 15-й 
				полосе (tr15)
				K -  коэффицент
				**************************************'''

				id=0 # Просто счетчик для адресации, выбирает из массива необходимые промежутки для текуш. станции
				for station_name in Hranges[0]:
					if station_name==tr.stats.station:
						K=Hranges[1][id]
						break
					id+=1

				if ((Fi>-1.41)and(Fi<-1.1)): # Если выполняется условие, то считаем высоту выброса
					print('Something wrong                                                                                             +')
					print('Fi = ',Fi,' | I = ',i, ' | amp_id = ',amp_id)

					H=K*Fi*abs(tr15)*(i-1)
					print('Height of ash strike = ',H)

		'''
		Запоминаем значения I и двигаем счетчик вперед
		'''
		amp_id+=1
		I = i
	tr_id+=1

			