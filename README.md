# MyPacks
## sqlcl.py
This file got from SDSS DR8 and adapted it for Python 3.
## spider\_set.py
    This file is a set of the functions in my spider program.
### spider\_WISeREP
	Get data from WISeREP by this spider script.

	It will place datafiles(e.g. .dat, .fits) in ./data_{groupName}.
	And it will place catalog_file in ./catalogs when catalogs_xpath is not an empty list .
	The fields of default catalog_file are 	fileName ,redshift ,targetName in program.

	root			the first url after your search,though it maybe very long.
					The default url is set to get the data of SDSS SNe. 
	
	string_ls		the string that will be used in the function fix_by_string.
					That function will reserve items whose type is existing in this list.

	catalog_xpath		a list of other xpaths that point to information which you need.
					The default is redshift of the supernova.
					If it isn't needed ,you can make it be an empty list.

	You need the packages below to run this program:
	requests    lxml    selenium
	And, you need a chrome and a chromedriver.exe which is suit for your chrome .
	(Chromedriver can be downloaded in http://chromedriver.storage.googleapis.com/index.html .
	Then,you need add it into Enviromental Variables of your device.)

## ipynb2pdf.py
    This file got from https://www.jianshu.com/p/49a0c9f74d59

