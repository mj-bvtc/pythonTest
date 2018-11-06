# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs
import csv

tests={'German': [u'Straße',u'auslösen',u'zerstören'], 
       'French': [u'français',u'américaine',u'épais'], 
       'Chinese': [u'中國的',u'英語',u'美國人']}

with open('/tmp/utf.csv','w') as fout:
    writer=csv.writer(fout)    
    writer.writerows([tests.keys()])
    for row in zip(*tests.values()):
        row=[s.encode('utf-8') for s in row]
        writer.writerows([row])

with open('/tmp/utf.csv','r') as fin:
    reader=csv.reader(fin)
    for row in reader:
        temp=list(row)
        fmt=u'{:<15}'*len(temp)
        print fmt.format(*[s.decode('utf-8') for s in temp])

