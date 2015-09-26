
# manipulate the HTML files into DataFrames

# import relevant libraries
from main import *

def createDF(yr):
	f = "%s%s.html" % (data_prefix, yr) # grab the HTML file
	dfs = pd.read_html(f, attrs={'id':'passing'}, flavor=['bs4']) #, index_col = 'Tm') # parse as a list of DFs

	df = dfs[0] # grab the first DF from the list

	df = df[:-2] # take out the last two lines (Avg and Total?)]

	df['season'] = yr

	return df

def main():

	remove = ['QBR', 'Rk', 'G', 'GWD', 'Lng', '4QC', 'NY/A', 'ANY/A', 'AY/A', 'Sk', 'SkYds', 'Sk%', 'Rate', 'EXP']

	stats = [
		"Cmp",
		"Att",
		"Cmp%",
		"Yds",
		"TD",
		"TD%",
		"Int",
		"Int%",
		"Y/A",
		"Y/C",
		"Y/G"
		]

	# list of the z variables
	z_stats = ['z_' + x for x in stats]

	master = pd.DataFrame()

	# for yr in range(1998,2000):
	for yr in range(firstYear, lastYear):
		print yr
		# curDF = curDF.append(createDF(yr))
		curDF = createDF(yr)
		curDF = curDF.rename(columns={'Yds.1': 'SkYds'}, inplace=False) # rename relevant column names

		# take out blank columns (appear due to extra rows above and how the table is parsed)
		for x in xrange(0,len(curDF.columns)+1):
			colName = 'Unnamed: %d' % (x)
			try:
				curDF = curDF.drop(colName, axis=1, inplace=False)
			except:
				pass

		# remove unnecessary variables
		for x in remove:
			try:
				curDF = curDF.drop(x, axis=1, inplace=False)
			except:
				pass

		# rename Oilers to Titans
		curDF.reset_index(inplace=True)
		curDF.loc[(curDF['Tm'] == 'Tennessee Oilers'), 'Tm'] = 'Tennessee Titans'
		curDF.set_index(['Tm'], inplace=True)

		# convert these variables to ints which will get rid of the decimal
		toInt = ['Cmp', 'Att', 'Yds', 'TD', 'Int', 'Y/G']
		for x in toInt:
			curDF[x] = curDF[x].astype(int)

		curDF.reset_index(inplace=True)
		for i, stat in enumerate(stats):
			# s2 = pd.DataFrame(zscore(curDF.loc[(curDF['season'] == yr)][stat])).mean()
			curDF[z_stats[i]] = pd.DataFrame(zscore(curDF[stat]))

		master = master.append(curDF)

	master.reset_index(inplace=True)
	master.drop('level_0', axis=1, inplace=True)
	curDF.to_csv(test_csv)
	master.to_csv(test2_csv)
	master.to_csv(dfout)

	# list of teams
	teams = list(unique_everseen([x for x in original['Tm']]))

	# cumAvgDF contains the average z's over time, used for sorting purpose
	cumAvgDF = pd.DataFrame()
	for team in teams:
		zTeam = pd.DataFrame(master.loc[(master['Tm'] == team)][z_stats].mean()).transpose()
		zTeam['Tm'] = team
		cumAvgDF = pd.concat([cumAvgDF, zTeam])

	cumAvgDF.to_csv(cumAvgDF_csv)

    # create average for seasons DFavgSeasonDF = pd.DataFrame()
    avgSeasonDF = pd.DataFrame()
	for team in teams:
		zTeam = pd.DataFrame(master.loc[(master['Tm'] == team)][z_stats].mean()).transpose()
		zTeam['Tm'] = team
		avgSeasonDF = pd.concat([avgSeasonDF, zTeam])

	avgSeasonDF.to_csv(cumAvgDF_csv)


if __name__ == '__main__':
	main()
