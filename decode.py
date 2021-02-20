# Распаковка первых 48 байт и blockette`ов
fixedHeader=['']
# Если разделитель в порядквом номере - 42, то будет вот так
seqNumberDec=str(int.from_bytes(data[0:6],'big')).find('42')+2
fixedHeader[0]=str(int.from_bytes(data[0:6],'big'))[seqNumberDec:]
for i in unpack('>2c5s2s3s2s2H4B2H2h4Bi2H', data[6:48]):
    fixedHeader.append(i)

# Пока без нахождения иных блокитов.
# Каждый последующий блокит указан во 
# втором поле текущего блокита.
# Если там стоит '0', тогда блокитов больше нет
blockette_1000=[]
for i in unpack('>2H4B',data[48:56]):
    blockette_1000.append(i)

blockette_1001=[]
for i in unpack('>2HBb2B',data[56:64]):
    blockette_1001.append(i)
