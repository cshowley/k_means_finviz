import numpy as np
import urllib2
from bs4 import BeautifulSoup
import json
import argparse
import pandas as pd


def finviz(ticker):
	page = urllib2.urlopen('http://finviz.com/quote.ashx?t='+ticker.lower())
	soup = BeautifulSoup(page, 'html.parser')
	tableList = []
	for table in soup.find_all('table'):
		tableList.append(table.prettify())

	finviz = {}
	data = json.dumps(tableList[8]).split('\\n')
	switch = 0
	for i,j in enumerate(data):
		if i == 0:
			continue
		if j.strip()[0] != '<':
			if switch == 0:
				key = j.strip()
				finviz[key] = []
				switch = 1
			else:
				value = j.strip()
				if key == 'Volatility':
					value = value.split()
					value = [float(i.strip('%')) * 0.01 for i in value]
					finviz['Volatility low'] = value[0]
					finviz['Volatility high'] = value[1]
					finviz.pop('Volatility', None)
					switch = 0
					continue
				elif key == '52W Range':
					value = value.split('-')
					value = [float(i.strip()) for i in value]
					finviz['52W Range low'] = value[0]
					finviz['52W Range high'] = value[1]
					finviz.pop('52W Range', None)
					switch = 0
					continue
				elif key == 'Volume':
					value = int(value.replace(',',''))
				elif key in ('Market Cap','Income','Sales','Shs Outstand','Shs Float','Avg Volume'):
					if 'B' in value:
						value = float(value.replace('B','')) * 1e9
					elif 'M' in value:
						value = float(value.replace('M','')) * 1e6
					elif 'K' in value:
						value = float(value.replace('K','')) * 1e3
				elif '%' in value:
					value = float(value.replace('%','')) * 0.01
				else:
					try:
						value = float(value)
					except ValueError:
						pass
				if value == '-':
					value = np.nan
				finviz[key] = value
				switch = 0
	finviz.pop('"', None)
	finviz['Ticker'] = ticker
	return pd.Series(finviz)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('ticker')
	args = parser.parse_args()
	print finviz(args.ticker)
