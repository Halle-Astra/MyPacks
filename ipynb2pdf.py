'''Got this file from https://www.jianshu.com/p/49a0c9f74d59 and made it be suit for python3'''
import sys
import subprocess
import pdfkit
inputfile = sys.argv[1].replace(" ","\ ")
temp_html = inputfile[0:inputfile.rfind('.')]+'.html'
command = 'ipython nbconvert --to html ' + inputfile
subprocess.call(command,shell=True)
print('============success===========')
output_file =inputfile[0:inputfile.rfind('.')]+'.pdf'
pdfkit.from_file(temp_html,output_file)
subprocess.call('rm '+temp_html,shell=True)
