"""
grab html and create pandas DF from it
"""

from main import *

master = pd.DataFrame()
for yr in xrange(firstYear, lastYear):
	print yr
	yr = str(yr)
	f = "%s%s.html" % (data_prefix, yr)
	dfs = pd.read_html(f, attrs={'id':'games'}, flavor=['bs4'], skiprows=[5,10, 13])
	df = dfs[0]
	df.rename(columns={'Week': 'round', 'Winner/tie': 'won', 'Loser/tie': 'lost'}, inplace=True)
	df.drop(['Unnamed: 3', 'Unnamed: 5'], axis=1, inplace=True)

	df['season'] = yr
	master = master.append(df)

master.to_csv(playoffs_csv)
