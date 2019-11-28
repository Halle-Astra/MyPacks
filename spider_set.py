import requests as rq 
from lxml import etree
from selenium import webdriver
import os 

def Get_and_Save(root,save_path = './'):
    r = rq.get(root)
    r.encoding = r.apparent_encoding
    t = r.text
    filename = root.split('/')[-1]
    filepath = save_path+filename
    with open(filepath,'w') as f:
        f.write(t)
    print('File ',filepath,' is finished!')

def fix_by_string(class_ls ,href_ls,string_ls=['SN'],mode = 'or'):
    size = len(class_ls)
    class_ls_n = []
    href_ls_n = [] 
    for i in range(size):
        for j in range(len(string_ls)):
            string = string_ls[j]
            if string in class_ls[i]:
                if mode ==  'or':
                    class_ls_n.append(class_ls[i])
                    href_ls_n.append(href_ls[i])
                if mode == 'and':
                    if j != len(string_ls)-1:
                        continue
                    else:
                        class_ls_n.append(class_ls[i])
                        href_ls_n.append(href_ls[i])
    return class_ls_n,href_ls_n

def get_html(root,driver,isnew = True):
    if isnew :
        driver.get(root)
    t = driver.page_source
    html = etree.HTML(t)
    return html

def spider_WISeREP(root=None):
    '''Get data from WISeREP by this spider.
    
    The args needed is the first url after your search,though it maybe very long.
    The default url is set to get the data of SDSS SNe. 
    
    You need the packages below to run this program:
    requests    lxml    selenium'''
    
    if not root:
        root = 'https://wiserep.weizmann.ac.il/search/spectra?&name=&name_like=0&public=all&inserted_period_value=0&inserted_period_units=days&type%5B%5D=null&type_family%5B%5D=null&instruments%5B%5D=null&spectypes%5B%5D=10&qualityid%5B%5D=null&groupid%5B%5D=48&spectra_count=&redshift_min=&redshift_max=&obsdate_start%5Bdate%5D=&obsdate_end%5Bdate%5D=&spec_phase_min=&spec_phase_max=&spec_phase_unit=days&phase_types%5B%5D=null&filters%5B%5D=null&methods%5B%5D=null&wl_min=&wl_max=&obj_ids=&spec_ids=&ids_or=0&reporters=&publish=&contrib=&last_modified_start%5Bdate%5D=&last_modified_end%5Bdate%5D=&last_modified_modifier=&creation_start%5Bdate%5D=&creation_end%5Bdate%5D=&creation_modifier=&show_aggregated_spectra=0&show_all_spectra=0&table_phase_name=40&num_page=50&display%5Bobj_rep_internal_name%5D=1&display%5Bobj_type_family_name%5D=0&display%5Bobj_type_name%5D=1&display%5Bredshift%5D=1&display%5Bphases%5D=1&display%5Bexptime%5D=1&display%5Bobserver%5D=1&display%5Breducers%5D=1&display%5Bsource_group_name%5D=1&display%5Basciifile%5D=1&display%5Bfitsfile%5D=1&display%5Bspectype_name%5D=1&display%5Bquality_name%5D=1&display%5Bextinction_corr_name%5D=0&display%5Bflux_calib_name%5D=0&display%5Bwl_medium_name%5D=0&display%5Bgroups%5D=0&display%5Bpublic%5D=1&display%5Bend_pop_period%5D=0&display%5Breporters%5D=0&display%5Bpublish%5D=1&display%5Bcontrib%5D=0&display%5Bremarks%5D=0&display%5Bcreatedby%5D=1&display%5Bcreationdate%5D=1&display%5Bmodifiedby%5D=0&display%5Blastmodified%5D=0'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(root)
    html = get_html(root,driver,isnew = False)
    groupName = html.xpath('//*[@id="block-system-main"]/div/div[2]/div[3]/table/tbody/tr[1]/td[15]/text()')[0]
    save_path = 'data_'+groupName.replace(' ','_')+'/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    page_nums = html.xpath('//*[@id="block-system-main"]/div/div[2]/div[4]/ul/li/a/text()')
    nums_filters = ['>','>>']
    page_nums = [i  for i in page_nums if i not in nums_filters]
    page_nums = [eval(i) for i in page_nums]
    roots = [root]
    for i in page_nums:
        k = i-1
        roots.append(root.split('?')[0]+f'?&page={k}'+root.split('?')[1])
    class_ls_final = []
    href_ls_final = []
    for root_t in roots:
        html = get_html(root_t,driver)
        class_ls = html.xpath('//*[@id="block-system-main"]/div/div[2]/div[3]/table/tbody/tr/td[7]/text()')
        href_ls = html.xpath('//*[@id="block-system-main"]/div/div[2]/div[3]/table/tbody/tr/td[16]/span/a/@href')
        class_ls,href_ls = fix_by_string(class_ls,href_ls)
        class_ls_final+=class_ls
        href_ls_final+=href_ls
    driver.quit()
    for i in href_ls_final:
        Get_and_Save(i,save_path)