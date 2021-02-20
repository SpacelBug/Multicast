# Распаковка первых 48 байт и blockette`ов
flag=0
fixedHeader=['']
# Порядковый номер распакован не верно
for i in unpack('>6B2c5s2s3s2s2H4B2H2h4Bi2H', data[0:48]):
    if (flag < 6):
        fixedHeader[0]=fixedHeader[0]+str(i)
        flag=flag+1
    else:
        fixedHeader.append(i)

blockette_1000=[]
for i in unpack('>2H4B',data[48:56]):
    blockette_1000.append(i)

blockette_1001=[]
for i in unpack('>2HBb2B',data[56:64]):
    blockette_1001.append(i)
