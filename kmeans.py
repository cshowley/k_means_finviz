from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from finviz import *
import pandas as pd


# sp500 = pd.read_csv('sp500.csv')
nyse = pd.read_csv('NYSE.csv')
df = pd.DataFrame()
for i,ticker in enumerate(nyse.Symbol):
# for i,ticker in enumerate(sp500.Ticker):
	print ticker
	try:
		df = pd.concat([df, finviz(ticker)], 1)
	except:
		print 'Error :('

df = df.fillna(0).transpose()
df.to_csv('tmp.csv', index=None)
tmp = df.drop(['Ticker','Index','Optionable','Shortable','Earnings'], 1)

X = []
for i in range(len(tmp)):
	X.append(tmp.iloc[i].tolist())
X = np.array(X)

kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
output = list(kmeans.labels_)

pca = PCA(n_components=2).fit(X)
pca_2d = pca.transform(X)

plt.figure()
for i,ticker in enumerate(df.Ticker):
	print ticker, output[i]
	if output[i] == 0:
		plt.plot(pca_2d[i,0], pca_2d[i,1], '+r')
	elif output[i] == 1:
		plt.plot(pca_2d[i,0], pca_2d[i,1], 'ok')
	elif output[i] == 2:
		plt.plot(pca_2d[i,0], pca_2d[i,1], '*b')

plt.show()