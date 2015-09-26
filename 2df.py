# manipulate the HTML files into DataFrames


# f = "%s%s.html" % (data_prefix, str(firstYear))
# dfs = pd.read_html(f, attrs={'id':'passing'}, flavor=['bs4'], index_col='Tm')
# dfs[0].to_csv(test_csv)


# import relevant libraries
from main import *

# function to extract the relevant string from HTML
def getStrings(var, flag):
	# flag determines if the variable passed is a header or a row
	# info stores the string to clean
	if flag == 1:
		info = var.get("data-stat")
		# return var.get('data-stat')
	else:
		try:
			info = var.a.contents[0]
			# return var.a.contents[0]
		except:
			if len(var.contents)==0: # if its blank
				return ''
			else:
				info = var.contents[0]
				# return info

	# return a clean string
	# return info
	# print 'evaluating end'
	return str(info).replace("[u'", '').replace("']",'').replace('\\t','') \
		.replace('\\n','').replace('%','').replace(',','').replace('[u"','') \
		.replace('"]','').replace('[<strong>','').replace('</strong>]','').replace('\n','')

# create a dataframe for each year
# @profile
def createDF(soup, var, zName, statName):
	# take year
	# f = "%s%s.html" % (data_prefix, year)
	# soup = BeautifulSoup(open(f).read())

	# the table called result contains the relevant information
	# soup = soup.find('table',{'id':'passing'})

	# header tags are th
	headers = soup.find_all('th')
	# row tags are tr
	rows = soup.find_all('tr')
	# cols = soup.find_all('td')

	# get the information for each column from each row
	d = {} # dictionary to store each row's information as the row is processing
	dList = [] # list of dictionaries - one dictionary for each row

	# print cols
	# for i,header in enumerate(headers):
		# key = header.get('data-stat')
		# print key
		# rows = soup.find_all('tr')
		# d.clear()

		# iterate over rows
		# head = getStrings(headers[col],1)
		# for row in rows:
			# cell = getStrings(rows[col],0)
			# d[key] = cell

		# print d

	for row in rows:
		cols = row.find_all('td') # column tags are td
		d.clear() # initialize d for the row

		# iterate over columns
		for col in xrange(len(cols)):
			head = getStrings(headers[col],1) # get the header/key
			cell = getStrings(cols[col],0) # get the row info/value
			if len(cell) == 0:
				cell = 0
			# if head =='comebacks':
				# print cell
			d[head] = cell # add to the dictionary

		# add the current row to the list of rows
		# prevent all null rows
		if len(d) > 0:
			dList.append(copy.copy(d))

	# after putting all the rows together
	# NOW WE HAVE A DATAFRAME
	df = pd.DataFrame(dList)

	# come back and clean up for 'T' and such...
	df = df.convert_objects(convert_numeric=True) # convert to numeric datatypes

	# change Oilers to Titans
	df.loc[(df['team'] == 'Tennessee Oilers'), 'team'] = 'Tennessee Titans'
	df.sort('team', ascending=True, inplace = True)

	# create new df with the teams grouped correctly
	group = pd.DataFrame(df.groupby(by='team',as_index = True)[var].sum())
	# list of 'teams' not necessary in output
	excludeList = ['League Total','<strong>Avg Team</strong>', '<strong>Avg Tm/G</strong>']
	group = group[~group.index.isin(excludeList)]

	try:
		group[zName] = zscore(group[var]) # get the z score
	except:
		group[zName] = float('nan')
	group.rename(columns={var:statName}, inplace=True) # rename
	return group

# take year

# create params using the 2014 data
f = "%s%s.html" % (data_prefix, str(firstYear))
soup = BeautifulSoup(open(f).read())

# the table called result contains the relevant information
soup = soup.find('table',{'id':'passing'})

# header tags are th
headers = soup.find_all('th')

# row tags are tr
rows = soup.find_all('tr')

# get the information for each column from each row
d = {} # dictionary to store each row's information as the row is processing
dList = [] # list of dictionaries - one dictionary for each row

for row in rows:
	cols = row.find_all('td') # column tags are td
	d.clear() # initialize d for the row

	# iterate over columns
	for col in xrange(len(cols)):
		head = getStrings(headers[col],1) # get the header/key
		# cell = getStrings(cols[col],0) # get the row info/value
		d[head] = None

	# add the current row to the list of rows
	# prevent all null rows
	if len(d) > 0:
		dList.append(copy.copy(d))

# after putting all the rows together
# NOW WE HAVE A DATAFRAME
df = pd.DataFrame(dList)
params = list(df.columns)
params.remove('team')
params.remove('ranker')
params.remove('qbr')
params.remove('g')
params.remove('gwd')
params.remove('pass_long')
params.remove('comebacks')
# print params


members = ['z','s'] # list of the types of names I will need to store for each statistic

master = pd.DataFrame()
var_dict = { p:{ v:[] for v in members} for p in params }

# initialize each key (ex: pass_yds) with var_list
for year in range(firstYear, lastYear):
# for year in range(1998,1999):
	f = "%s%s.html" % (data_prefix, year)
	soup = BeautifulSoup(open(f).read())
	soup = soup.find('table',{'id':'passing'})
	print 'Year: %d' % year
	for p in params:
		print '\tp: %s' % p
		zName = '%s_z_%s' % (str(year),p) # create a variable name for the z score
		statName = '%s_%s' % (str(year), p) # create a new variable name with the current year
		var_dict[p]['z'].append(zName)
		var_dict[p]['s'].append(statName)

		master = master.join(createDF(soup, p, zName, statName), how='outer')
		stat_avgName = 'stat_avg_%s' % (p) # create new variable for average over years
		z_avgName = 'z_avg_%s' % (p) # create new variable for average over years
		var_dict[p]['stat_avg'] = stat_avgName
		var_dict[p]['z_avg'] = z_avgName

for p in params:
	statDF = master[var_dict[p]['s']]
	zDF = master[var_dict[p]['z']]

	master[var_dict[p]['stat_avg']] = statDF.mean(axis=1)
	master[var_dict[p]['z_avg']] = zDF.mean(axis=1)

# print var_dict
# output the dataframe as a csv
cout = '%sdf.csv' % data_prefix
master.to_csv(cout)

import json
str_params = '%sparams.json' % (data_prefix)
str_members = '%smembers.json' % (data_prefix)
str_var_dict = '%svar_dict.json' % (data_prefix)

with open(str_params, 'w') as fp:
    json.dump(params, fp)

with open(str_members, 'w') as fp:
    json.dump(members, fp)

with open(str_var_dict, 'w') as fp:
    json.dump(var_dict, fp)
