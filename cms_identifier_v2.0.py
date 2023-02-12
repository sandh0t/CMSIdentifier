##!/usr/bin/python
#
# Version 1 


# verify whether the python libraries are imported successfully or not!


# install prettytabel lib using the display table as result
# sudo apt-get install python-prettytable
import sys, re, socket, string, fileinput, requests

try:
	import xlwt
except ImportError:
	print "[-] program could not find module : xlwt" 
	print "[!] use this cmd to add this module: apt-get install python-xlwt "
	sys.exit (1)

try:
	from prettytable import PrettyTable
except ImportError:
	print "[-] program could not find module : prettytable" 
	print "[!] use this cmd to add this module: apt-get install python-prettytable "
	sys.exit (1)
	
try:
	from xml.dom import minidom
except ImportError:
	print "[-] program could not find module : minidom" 
	sys.exit (1)	


try:
	import urllib2
except ImportError:
	print "[-] program could not find module : urllib2" 
	sys.exit (1)

import sys, re, socket, string, fileinput
import codecs
from urllib2 import Request, urlopen, URLError, HTTPError

# python version check

def check_python():
        version = sys.version_info
        if version[:2] != (2,7):
                print "[-] CMS Identifier is written in Python 2.7.x . use that version!"
                sys.exit(0)


# Prints usage
def print_usage():
    print "Usage:"
    print "        -u <URL>      Provid the Target URL"
    print "        -l <List>     Provid List of Targets URLs"
    print "        -o <File>     Save Output to a file"
    print "        -s            Sort Result by CMS name" 
    print "        -x            Generate a XLS file named 'out.xls'"    
    print "        --help        (displays this text)"
    print "\n\n\n"

    return
    
    
#Prints banner
def print_banner():
    print "\n\n\n\n\n"
    print "\033[1;32m         ***  CMS Identifier    Version: 2.0  *** \033[1;m"
    print "\n"
    print '\033[1;31m                                  /$$$$$$       /$$                       /$$     /$$  /$$$$$$  /$$                    \033[1;m'
    print '\033[1;31m                                 |_  $$_/      | $$                      | $$    |__/ /$$__  $$|__/                    \033[1;m'
    print '\033[1;31m  /$$$$$$$ /$$$$$$/$$$$   /$$$$$$$ | $$    /$$$$$$$  /$$$$$$  /$$$$$$$  /$$$$$$   /$$| $$  \__/ /$$  /$$$$$$   /$$$$$$ \033[1;m'
    print '\033[1;31m /$$_____/| $$_  $$_  $$ /$$_____/ | $$   /$$__  $$ /$$__  $$| $$__  $$|_  $$_/  | $$| $$$$    | $$ /$$__  $$ /$$__  $$\033[1;m'
    print '\033[1;31m| $$      | $$ \ $$ \ $$|  $$$$$$  | $$  | $$  | $$| $$$$$$$$| $$  \ $$  | $$    | $$| $$_/    | $$| $$$$$$$$| $$  \__/\033[1;m'
    print '\033[1;31m| $$      | $$ | $$ | $$ \____  $$ | $$  | $$  | $$| $$_____/| $$  | $$  | $$ /$$| $$| $$      | $$| $$_____/| $$      \033[1;m'
    print '\033[1;31m|  $$$$$$$| $$ | $$ | $$ /$$$$$$$//$$$$$$|  $$$$$$$|  $$$$$$$| $$  | $$  |  $$$$/| $$| $$      | $$|  $$$$$$$| $$      \033[1;m'
    print '\033[1;31m \_______/|__/ |__/ |__/|_______/|______/ \_______/ \_______/|__/  |__/   \___/  |__/|__/      |__/ \_______/|__/      \033[1;m'
    print '\033[1;31m                                                                                                                       \033[1;m'
    print "\n\n\n"

	
    
    return

##############################################################################################################
# Validate url syantexe 
def valid_url( url ):
    if url.startswith("http://") or url.startswith("https://") :
      url = url
    else:
      url = "http://" + url;
    return url

    
########################################################################################################
######################                       FRAMEWORK                       ###########################
########################################################################################################    
# Testing if URL is reachable, with error handling  and Identifu the server and framework name
def check_framework( host ):
  
    res = "False"
    ip = ""
    frm = ""
    srv = "-"
    title = "-"
    # At first we validate if the host does exist in DNS entry by checking for socket info
    if host.endswith('/'):
		host = host[:-1]
    if "http://" in host:
		host = host.replace('http://','')
    if "https://" in host:
		host = host.replace('https://','')			
    host = host.split('/')
    host = host[0]
    host = host.split(':')
    host = host[0]
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        ip = "the host does not exist !!"
        
    # then we test if we can actually reach the provided URL      
    url = valid_url(host) 
    try:
        req = requests.get(url, timeout=10)
        # HTTP errors are not raised by default, this statement does that
        req.raise_for_status()
        res = True
    except requests.HTTPError as e:
        res = "False, Checking internet connection failed, status code {0}.".format(e.response.status_code)
    except requests.ConnectionError:
        res = "False,  No internet connection available."
    except :
		res = False
    
    if res: 
		try:
			response = urllib2.urlopen(url,timeout=10)
			# Identify the server
			if "server" in response.info():
				srv =  response.info()['server']
			else:
				srv =  "Can't Identify"
			# Identify the framework name
			if "x-powered-by" in response.info():
				frm = frm + response.info()['x-powered-by'] 
			elif "PHP" in response.info():
				frm = frm +   "PHP" 
			elif "X-AspNet-Version" in response.info():
				frm = frm +   "ASP.NET v"+ response.info()['x-aspnet-version']
			elif "ASP" in response.info():
				frm = frm +   "PHP"
			else:
				frm =  "Can't Identify"
		except :
			res = res
			pass				
		# Get page title 	
			try:
				resp_split = response.read()
				str_title = "<" + "/" + "title" + ">"
				resp_split = resp_split.split("<title>")
				resp_split = resp_split[1].split(str_title)
				title = resp_split[0]
				title = title.replace("\t","")
				title = title.replace("\r","")
				title = title.replace("\n","")
				title = unicode(title, errors='ignore')
			except :
				pass
	    
	                
    return res, ip, srv, frm, title

    
########################################################################################################
######################                        Joomla                         ###########################
########################################################################################################
# Function to check if the WebSite is using Joomla
def check_joomla( str ):
    joom_valid="False"
    joom_version=""
    v = 1
    str_xml = str + "/language/en-GB/en-GB.xml"
    try:
	response_html = urllib2.urlopen(str, timeout=10)
	response_xml = urllib2.urlopen(str_xml, timeout=10)
	xml_file = minidom.parse(response_xml)
    except :
	v = 0
	pass
    else:
	if v > 0:
	    if xml_file.getElementsByTagName("version").length > 0:
	        joom_version = xml_file.getElementsByTagName('version')[0].toxml()
	        joom_version = joom_version.replace('<version>','').replace('</version>','')
	        joom_valid="True"
		
	if "option=com_content" in response_html.read() and v == 0:
	    joom_valid="True"
	    joom_version=""
	   
    if joom_valid == "False":
	joom_version=""
               
    return joom_valid, joom_version
 
########################################################################################################
######################                        Drupal                         ###########################
########################################################################################################
# Function to check if the WebSite is using Drupal
def check_drupal( str ):
    drupal_valid="False"
    drupal_version=""
    resp=""
    v = 1
    str_txt = str + "/CHANGELOG.txt"
    try:
	response = urllib2.urlopen(str, timeout=10)
	resp = response.read()
	response_txt = urllib2.urlopen(str_txt, timeout=10)
	res_txt = response_txt.read()
    except :
	v = 0
	pass
    finally:
	if v > 0:
	    if "Drupal" in res_txt:
		drupal_valid="True"
		resp_txt_split = res_txt.split()
		for elem in resp_txt_split:
			if elem == 'Drupal':
				r = resp_txt_split[resp_txt_split.index('Drupal')+1]
				drupal_version =  r[:-1]
				break
	
	if ("Drupal.settings" in resp) and (v == 0):
	    drupal_valid="True"
	    drupal_version=""
	    
    if drupal_valid == "False":
	    drupal_version=""
               
    return drupal_valid, drupal_version
    
########################################################################################################
######################                       WordPress                       ###########################
########################################################################################################
def check_wordpress( str ):
    wordpress_valid=""
    wordpress_version=""
    
    try:
	response = urllib2.urlopen(str, timeout=10)
    except :
	pass
    else:
	resp = response.read()
	#res_txt = response_txt.read()
	str1 = "/" + "wp-content"
	str2 = "/" + "wp-admin"
	str3 = "/" + "wp-includes"
	if ( str1 in resp ) or ( str2 in resp) or ( str3 in resp):
	    wordpress_valid="True"
	    resp_split = resp.split()
	    for elem in resp_split:
		if elem == 'content="WordPress':
		      r = resp_split[resp_split.index('content="WordPress')+1]
		      wordpress_version =  r[:-1]
		      break
		
    if wordpress_valid == "":
	    wordpress_valid = "False"
	    wordpress_version_version=""
               
    return wordpress_valid, wordpress_version
    
########################################################################################################
######################                         SPIP                          ###########################
########################################################################################################
#SPIP
def check_spip( str ):
    spip_valid=""
    spip_version="-"
    
    try:
	response = urllib2.urlopen(str + "index.php", timeout=10)
    except :
	pass
    else:
	resp = response.read()
	#res_txt = response_txt.read()
	if ( "spip.php?" in resp ):
	    spip_valid="True"
	    resp_split = resp.split()
	    for elem in resp_split:
		if elem == 'content="SPIP':
		      r = resp_split[resp_split.index('content="SPIP')+1]
		      spip_version =  r
		      break
		
    if spip_valid == "":
	    spip_valid = "False"
	    spip_version_version="-"
               
    return spip_valid, spip_version
    
########################################################################################################
######################                       DotNetNuke                      ###########################
########################################################################################################
# DotNetNuke
def check_dotnetnuke( str ):
    dotnetnuke_valid=""
    dotnetnuke_version=""    
    resp=""
    try:
		response = urllib2.urlopen(str + "/Default.aspx" , timeout=10)
        #response_txt = urllib2.urlopen(str_txt)
    except :
		pass
    else:
	resp = response.read()
	string1 = "/" + "DesktopModules" + "/"
	string2 = "/" + "/Portals/0" + "/"
	if ( 'content="DotNetNuke' in resp ) or ( string1 in resp ) or ( string2 in resp ):
	    dotnetnuke_valid="True"
	    		
    if dotnetnuke_valid != "True":
	    dotnetnuke_valid = "False"
	    dotnetnuke_version=""
               
    return dotnetnuke_valid, dotnetnuke_version

########################################################################################################
######################                       SharePoint                      ###########################
########################################################################################################
# check if the CMS is SharePoint 
def check_sharepoint( str ):
    sharepoint_valid=""
    sharepoint_version=""
    resp=""
    try:
	response = urllib2.urlopen(str, timeout=10)
    except :
	pass
    else:
	resp = response.read()
	inf = response.info()
	if "MicrosoftSharePointTeamServices" in inf:
	    sharepoint_valid="True"
	    sharepoint_version=response.info()['MicrosoftSharePointTeamServices']
	elif "\_layouts\1036" in resp or ( 'content="Microsoft SharePoint' in resp ):
	    sharepoint_valid="True"
	
    if sharepoint_valid == "":
	    sharepoint_valid = "False"
	    sharepoint_version=""
               
    return sharepoint_valid, sharepoint_version
########################################################################################################
######################                         Magento                       ###########################
########################################################################################################
# check if the CMS is Magento 
def check_magento( str ):
    magento_valid=""
    magento_version="" 
    resp=""   
    str_admin = str + "/admin/"
    try:
		response = urllib2.urlopen(str, timeout=10)
		response_admin = urllib2.urlopen(str_admin, timeout=10)
		response_admin = urllib2.urlopen(str_admin, timeout=10)
		resp = response.read()
		resp_admin = response_admin.read()
		stri = "skin" + "/" + "frontend" + "/"
		if ( "Magento" in resp_admin ):
			magento_valid="True"
		elif stri in resp:
			magento_valid = "True"
		else:
			magento_valid = "False"			
    except :
		pass 
	
    return magento_valid, magento_version
########################################################################################################
######################                       Check CMS                       ########################### 
########################################################################################################	
def check_cms( url ):
    cms, ver = check_joomla(url)
    if res == True:
	    cms, ver = check_joomla(provided_url)
	    if cms == "True":
	        cms = "Joomla "
	    else:
	        cms, ver = check_drupal(provided_url)
	        if cms == "True":
	        	cms = "Drupal "
	        else:
			cms, ver = check_wordpress(provided_url)
			if cms == "True":
			    cms = "WordPress "
			else:
			    cms, ver = check_dotnetnuke(provided_url)
			    if cms == "True":
			        cms = "DotNetNuke "
			    else:
			        cms, ver =  check_sharepoint(provided_url)
				if cms == "True":
				    cms = "SharePoint "
				else:
				    cms, ver =  check_magento(provided_url)
				    if cms == "True":
						cms = "Magento "
			            else:
						cms = "Can't Identify !! "
				    
    cms = cms + ver
		
    return cms

 ##############################################################################################################
# Checking if argument was provided
table = ""
sort = "False"
w = ""
ws = ""
outxls = ""
cms = "" 
if len(sys.argv) <=1:
    print_usage()
    sys.exit(1)
    
for elem in sys.argv:
    if elem == "-s":
	sort = "True" 

for elem in sys.argv:
    if elem == "-x":
	outxls = "True"    
	w = xlwt.Workbook(encoding='utf-8')
	ws = w.add_sheet('Sheet')
	style_string = "font: bold on; borders: bottom dashed"
	style = xlwt.easyxf(style_string)
	ws.write(0, 0, "Id", style=style)
	ws.write(0, 1, "Target", style=style)
	ws.write(0, 2, "Is Website Up", style=style)
	ws.write(0, 3, "IP Address", style=style)
	ws.write(0, 4, "Server", style=style)
	ws.write(0, 5, "Framework", style=style)
	ws.write(0, 6, "CMS", style=style)	
	
	
    
for arg in sys.argv:
    # Checking if help was called
    if arg == "--help":
        print_usage()
        sys.exit(1)
    
    # Checking from URL 
    if arg == "-u":
	cms = "-"
	ver = "-"
        provided_url = sys.argv[2]
        print_banner() 
        print_usage()
	provided_url = valid_url(provided_url) 
	res, ip,  srv, frm, title  = check_framework(provided_url)	
	
	if outxls=="True":
		ws.write(1, 0, 1)
		ws.write(1, 1, provided_url)
		ws.write(1, 2, str(res))
		ws.write(1, 3, ip)
		ws.write(1, 4, srv)
		ws.write(1, 5, frm)
		ws.write(1, 6, cms)
		w.save('out.xls')
		
	if res == True:
	    cms = check_cms(provided_url)
	    print "\033[1;32m[+]\033[1;m" + "\033[1;36m" +  provided_url + "\033[1;m" + "  Is Website Up: " + "\033[1;33m" + str(res) + "\033[1;m"    + "  IP Address: " + "\033[1;33m" + ip + "\033[1;m"    + "  Server: " + "\033[1;33m" + srv + "\033[1;m" + " Framework: " +  "\033[1;33m" + frm + "\033[1;m" + "  CMS: " +  "\033[1;32m" + cms + "\033[1;m"
	else:
	    print "\033[1;31m[-]\033[1;m " +  "\033[1;36m" +  provided_url + "\033[1;m" + "  Is Website Up: " + "\033[1;33m" + str(res) + "\033[1;m"
	
        
        
    # Checking from LIST
    if arg == "-l":
        provided_list = sys.argv[2]
        print_banner() 
        print_usage()
        Id = 0
        #print_banner()
        
        list = open(provided_list , "r" )
        # Defining Table Fileds and Style
        x = PrettyTable(["Id", "Target", "Valid Target", "IP Address", "Server", "Framework", "CMS"])
        #x = PrettyTable(["Id", "Target", "Valid Target", "Title", "Server", "Framework", "CMS"])
	x.align["Target"] = "l" # Left align target 
	x.align["Server"] = "l" # Left align server
	x.align["CMS"] = "l"
	x.align["Framework"] = "l"
	#x.padding_width = 1 # One space between column edges and contents (default)
	x.hrules = 1

	i = 1		
	try:
	    for line in list:
		line = line.strip()
		Id = Id + 1
		if not line == '':
		    line = valid_url(line)
		    provided_url = line
		    res, ip, srv, frm, title  = check_framework(provided_url)
		 
		    if res == True:
				cms = check_cms(provided_url)
				print "\033[1;32m[+]\033[1;m" + "\033[1;36m" +  provided_url + "\033[1;m" + "  Is Website Up: " + "\033[1;33m" + str(res) + "\033[1;m"    + "  IP Address: " + "\033[1;33m" + ip + "\033[1;m"    + "  Server: " + "\033[1;33m" + srv + "\033[1;m" + " Framework: " +  "\033[1;33m" + frm + "\033[1;m" + "  CMS: " +  "\033[1;32m" + cms + "\033[1;m"
		    else:
				print "\033[1;31m[-]\033[1;m " +  "\033[1;36m" +  provided_url + "\033[1;m" + "  Is Website Up: " + "\033[1;33m" + str(res) + "\033[1;m"
			
		    if outxls=="True":
				ws.write(Id, 0, Id)
				ws.write(Id, 1, provided_url)
				ws.write(Id, 2, str(res))
				ws.write(Id, 3, ip)
				ws.write(Id, 4, srv)
				ws.write(Id, 5, frm)
				ws.write(Id, 6, cms)
				
			#if len(srv) > 20:
			    #srv = srv [:20] + "..."
			    
			#if len(frm) > 20:
			    #frm = frm[:20] + "..."
			    
		    x.add_row([Id, provided_url, res, ip,  srv, frm, cms])
		else:
			print "\033[1;31m" + "[-] " + provided_url + "   unreachable !!!" + "\033[1;m"
			#x.add_row([Id, provided_url, "False",  ip , "-", "-", "-", ])
			x.add_row([Id, provided_url, "False", "-", "-", "-", "-" ])
			if outxls=="True":
				ws.write(Id, 0, Id)
				ws.write(Id, 1, provided_url)
				ws.write(Id, 2, "False")
				ws.write(Id, 3, "-")
				ws.write(Id, 4, "-")
				ws.write(Id, 5, "-")
				ws.write(Id, 6, "-")
	
	except KeyboardInterrupt:
	    print "Exiting now ... !!"
	    if sort == "True":
		table = x.get_string(sortby="CMS")
	    else:
		table = x.get_string()
		
	    print "\n\n\n" + "\033[1;32m" + table + "\033[1;m " + "\n\n\n"
	    list.close()
	    sys.exit(1)
	    
	finally:
	    table = x.get_string(sortby="CMS")
	    if sort == "True":
		table = x.get_string(sortby="CMS")
	    else:
		table = x.get_string()
	
	    print "\n\n\n" + "\033[1;32m" + table + "\033[1;m " + "\n\n\n"
	    list.close()
	    
	if outxls =="True":
		w.save('out.xls')	
		
    if arg == "-o":
	provided_file = sys.argv[4]
	f = codecs.open(provided_file, "w", "utf-8")
	f.truncate()
	#table = unicode(table, errors='ignore')
	f.write("\n\n\n" + table+ "\n\n\n")
        f.close()
        sys.exit(1)
        
	    


