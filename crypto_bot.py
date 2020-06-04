import requests
import time
from datetime import datetime as d
import datetime
from operator import itemgetter
import json

#Crypto_bot
class Bot:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start': '1',
            'limit': '100',
            'convert': 'USD',
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'YOUR_KEY'
        }
        self.all_data = {}
        self.elab_data = {}
    #Richiesta APIs CoinMarket
    def fetchCurrenciesData(self):
            self.all_data = requests.get(url=self.url, headers=self.headers, params=self.params).json()
    #Analisi ed elaborazione dei dati ricevuti
    def analisi(self):
        res = self.all_data
        try:
            timestamp = datetime.date.today()
            max = -1
            list_supp = []
            list_symbol = {}
            sum_first_twenty = 0
            sum_volum_24h = 0
            for x in res['data']:
                if float(x['quote']['USD']['volume_24h']) > max:
                    max = x['quote']['USD']['volume_24h']
                    max_name = x['slug']
                if int(x['cmc_rank']) <= 20:
                    sum_first_twenty += float(x['quote']['USD']['price'])
                    list_symbol.update( {x['slug']:x['quote']['USD']['price']})
                if float(x['quote']['USD']['volume_24h']) > 76000000.0:
                    sum_volum_24h += float(x['quote']['USD']['price'])
                list_supp.append([float(x['quote']['USD']['percent_change_24h']), x['slug']])
            list_supp.sort(key=itemgetter(0), reverse=True)
            today = timestamp.strftime("%m-%d-%Y")
            res_list = {'date': today,
                        'max': max,
                        'max_name': max_name,
                        'sumf': sum_first_twenty,
                        'sumv': sum_volum_24h,
                        'best': list_supp[:10],
                        'worst': list_supp[-10:],
                        'top': list_symbol
                        }
            with open('{0}.json'.format(today), "w") as outfile:
                json.dump(res_list, outfile)
            self.elab_data = res_list
        except ValueError:
            print("Errore elaborazione dati")
    #Stampa dei risultati
    def print_res(self):
        res = self.elab_data
        try:
            print('La criptovaluta con il volume maggiore (in $) delle ultime 24 ore è',res['max_name'],'con',res['max'],'$')
            print("---")
            print('Denaro per top 20:',res['sumf'],'$')
            print("---")
            print('Denato per top 20 volume: ',res['sumv'],'$')
            print("---")
            print('Top 10 incremento')
            for x in res['best']:
                print(x[1],': ',x[0],'%')
            print("---")
            print('Worst 10 incremento')
            for x in res['worst']:
                print(x[1],': ',x[0],'%')
            print("---")
        except:
            print('Errore stampa risultati')
    #Confronto dati odierni con quelli passati
    def comparison(self):
        res = self.elab_data
        try:
            today = d.strptime(res['date'], '%m-%d-%Y').date()
            yesterday = today - datetime.timedelta(days=1)
            yesterday = yesterday.strftime("%m-%d-%Y")
            prec = json.load(open('{0}.json'.format(yesterday), "r"))
            sum_prec = 0
            sum_today = 0
            num_crypto = 0
            for x in res['top'].keys():
                y = prec['top'].get(x, -1)
                if y >= 0:
                    sum_prec += y
                    sum_today += res['top'].get(x)
                    num_crypto += 1
            if sum_today >= sum_prec:
                diff_perc = 100 - (sum_prec * 100) / sum_today
            else:
                diff_perc = -(100 - (sum_today * 100) / sum_prec)
            print("Differenza in percentuale rispetto a ieri:",diff_perc)
            print("---")
            print("Crypto in comune:",num_crypto,"su 20")
        except:
            print("Errore comparazione percentuale")
#Esecuzione del programma
if __name__ == "__main__":
    #while(1): rimuovere per eseguire un ciclo infinito
        exbot = Bot()
        exbot.fetchCurrenciesData()
        exbot.analisi()
        exbot.print_res()
        exbot.comparison()
        #time.sleep(5) rimuovere per interrompere il processo ogni x secondi
