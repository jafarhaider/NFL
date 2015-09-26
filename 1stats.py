# get all QB stats from NFL.com since 1998 - P. Manning's first year

# import necessary libraries
from main import *

# create file to save the URLs for future use

c = "%sDownload_Check.csv" % output_prefix # file name
check_file = open(c, 'w') # create the actual file
check_file_object = csv.writer(check_file) # the file object which is acted upon
check_file_object.writerow(["Year", "URL"]) # header row

# declare functions
# gets statistics page from pro-football-reference.com and saves it to computer
def getPFR(year):
    print "%s:" % year
    # two parts of the URL for team level data
    url1 = 'http://www.pro-football-reference.com/years/'
    url2 = '/'
    
    # combine with the year
    url = "%s%s%s" % (url1, year, url2)
    
    # write the url to the output and the check file for posterity
    print "\tURL:\n\t\t%s" % url
    check_file_object.writerow([year,url])
    
    # file where the current year will be saved
    path = "%s%s.html" % (data_prefix, year)
    
    # access the website
    r = urllib3.PoolManager().request('GET', url)
    
    # make sure that the link worked correctly. if it doesn't, the program exits
    if r.status != 200:
        print "Exiting because status is not 200. Status: %s" % str(r.status)
        sys.exit()

    # write the webpage to the file specified above
    with open(path, 'w') as out:
        out.write(r.data)

    # release the connection...necessary?
    r.release_conn()
    
    # notify the user
    print "\tStatus:\n\t\tCOMPLETE\n\n"
    
# call function for given years
for year in xrange(firstYear,lastYear):
    getPFR(str(year))

# close the check file and notify the user
check_file.close()
print "DONE"