import pandas_datareader.data as web
import datetime as dt
import requests
import ssl
import pandas as pd


ssl._create_default_https_context = ssl._create_unverified_context
#The following lines fix a recent DataReader problem for yahoo finance
USER_AGENT = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                   ' Chrome/91.0.4472.124 Safari/537.36')
    }
sesh = requests.Session()
sesh.headers.update(USER_AGENT)

def historico(stock,ano=1980,mes=1,dia=1):
  start= dt.datetime(ano,mes,dia)
  end=dt.datetime.today()
  df = web.DataReader(stock,'yahoo', start=start,end=end, session=sesh)
  df['var_diaria']=round(df['Adj Close'].pct_change()*100,2)
  return df


qqq=historico('qqq')
caidas=qqq[qqq['var_diaria']<-5]
caidas['año']=caidas.index.year
caidas_5puntos=pd.DataFrame(caidas[caidas['año']>2012]['var_diaria'])
caidas.index[0]+dt.timedelta(days=1)
caidas_5puntos.columns=['Caídas mayores a 5%']

fechas=caidas_5puntos.index
fechas_nuevo=list()
for fecha in fechas:
  if fecha.weekday()==4:
    fecha = fecha+dt.timedelta(days=3)
    fechas_nuevo.append(fecha)
  else:
    fecha = fecha+dt.timedelta(days=1)
    fechas_nuevo.append(fecha)



dia_post=historico('qqq')
dia_post=dia_post.filter(items=fechas_nuevo,axis=0)
dia_post=pd.DataFrame(dia_post['var_diaria'])
dia_post.columns=['Día posterior']

print(caidas_5puntos)
print(dia_post)

