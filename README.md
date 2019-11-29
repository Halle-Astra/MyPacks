# MyPacks
## sqlcl.py
This file got from SDSS DR8 and adapted it for Python 3.
## spider\_set.py
### spider\_WISeREP
    spider_WISeREP(root=None,catalog_xpath = [...])
    
    Get data from WISeREP by this spider.
    
    The first arg is the first url after your search,though it maybe very long.
    The default url is set to get the data of SDSS SNe. 
    
    The second arg is a list of other xpaths that point to information which you need.
    The default is redshift of the supernova.
    If it isn't needed ,you can make it be a empty list but may be wrong.
    
    You need the packages below to run this program:
    requests    lxml    selenium
