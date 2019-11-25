import subprocess
import os
import re
from datetime import datetime
import glob
import os.path

###find substring between two sub-strings
def find_between_r(s, first, last):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

#BlocoEsquerda

#warcit --fixed-dt 20121031235959 http://www.acores.bloco.org/ ./blocoEsquerda/

##DinisAlves2018


###Problems
## Folders considered: ./APP-2012 and ./APFF-2013 (homepages)
## New folders required, for each .html/htm file was create a folder with the corresponding timestamp. 
## For instance, I created a new folder "01-08-2012-05h08m" and all files with this timestamp in the suffixed were included.
## .webarchive files need to be save with safari and change the enconding on chaset of the .html by hand.

##Pre-step
# Some html files do not have the corresponding images and css/js.
# So, if it does not exist the folder "www_portosdeportugal_pt-XXXXXXX_ficheiros", in the html file, the css/js were referenced online.

mypath = "./APP-2012" 
URL_Main = "http://www.portosdeportugal.pt/"

timestamp_processed = []
for subdir, dirs, files in os.walk(mypath):
    for file in files:
        file_name = os.path.join(subdir, file)
        if "htm" in file_name and ("www_portosdeportugal_pt" in file_name or "index" in file_name):
            string = os.path.join(subdir, file) 
            result = string.split("/")
            string_find = os.path.join(subdir, "www_portosdeportugal_pt-" + result[2] + "_ficheiros")
            if not os.path.isdir(string_find):
                f = open(file_name, "rt", encoding='ISO-8859-1')
                filedata = f.read()
                f.close()
                string = find_between_r(filedata, "<title>www.portosdeportugal.pt</title>", "</script><script type=\"text/javascript\">" )
                all_replace = "<title>www.portosdeportugal.pt</title>" + string + "</script><script type=\"text/javascript\">"
                replace = "<title>www.portosdeportugal.pt</title>\n<link href=\"http://www.portosdeportugal.pt/css/dropdown.css\" rel=\"stylesheet\" type=\"text/css\">\n<link href=\"http://www.portosdeportugal.pt/css/current.css\" rel=\"stylesheet\" type=\"text/css\">\n<link href=\"http://www.portosdeportugal.pt/css/modalbox.css\" rel=\"stylesheet\" type=\"text/css\">\n<link href=\"http://www.portosdeportugal.pt/css/global.css\" rel=\"stylesheet\" type=\"text/css\">\n<link href=\"http://www.portosdeportugal.pt/css/CalendarPopup.css\" rel=\"stylesheet\" type=\"text/css\">\n<script src=\"https://connect.facebook.net/pt_PT/all.js?hash=8fd8fc7a8866f62a46936fb70da2dc4e\" async=\"\"></script><script id=\"facebook-jssdk\" src=\"//connect.facebook.net/pt_PT/all.js#xfbml=1\"></script><script language=\"javascript\" src=\"http://www.portosdeportugal.pt/jquery/jquery-1.0.1.pack.js\"></script>\n<script type=\"text/javascript\" src=\"http://www.portosdeportugal.pt/js/modalbox/prototype.js\"></script>\n<script type=\"text/javascript\" src=\"http://www.portosdeportugal.pt/js/modalbox/scriptaculous.js?load=effects\"></script><script type=\"text/javascript\" src=\"http://www.portosdeportugal.pt/js/modalbox/effects.js\"></script><script type=\"text/javascript\" src=\"http://www.portosdeportugal.pt/js/modalbox/effects.js\"></script>\n<script type=\"text/javascript\" src=\"http://www.portosdeportugal.pt/js/CalendarPopup.js\"></script><script type=\"text/javascript\" src=\"http://www.portosdeportugal.pt/js/modalbox.js\"></script><script type=\"text/javascript\" src=\"http://www.portosdeportugal.pt/js/global.js\"></script><script type=\"text/javascript\">"
                newdata = filedata.replace(all_replace, replace)
                f = open(file_name,'w', encoding='ISO-8859-1')
                f.write(newdata)
                f.close()


##Script_To_PortosDePortugal


mypath = "./APP-2012" 
URL_Main = "http://www.portosdeportugal.pt/"

timestamp_processed = []
for subdir, dirs, files in os.walk(mypath):
    for file in files:
        file_name = os.path.join(subdir, file)
        if "htm" in file_name and ("www_portosdeportugal_pt" in file_name or "index" in file_name):
            string = os.path.join(subdir, file) 
            result = string.split("/")
            day = re.split('-', result[2])
            if len(day) == 4:
                hours = re.findall(r'\d+', day[3])
                timestamp = day[2] + day[1] + day[0] + hours[0] + hours[1] + "00"
            else:
                timestamp = day[2] + day[1] + day[0] + "235959"
            if timestamp not in timestamp_processed:
                folder = mypath + "/" + result[2] + "/"
                if "index" not in file_name:
                    result = string.split("/")
                    index_path =  '/'.join(result[0:len(result)-1]) + '/index.htm'
                    subprocess.run(["mv", file_name, index_path])
                subprocess.run(["warcit", "--fixed-dt", timestamp, URL_Main, folder])
                timestamp_processed.append(timestamp)


##Script_To_Porto_Figueira
##Porto da Figueira da Foz-15-02-2013-00h59m_ficheiros has change by hand

mypath = "./APFF-2013" 
URL_Main = "http://www.portofigueiradafoz.pt/"

timestamp_processed = []
for subdir, dirs, files in os.walk(mypath):
    for file in files:
        file_name = os.path.join(subdir, file)
        if "htm" in file_name and ("Porto da Figueira da Foz" in file_name or "index" in file_name or "portofigueiradafoz.pt" in file_name):
            string = os.path.join(subdir, file) 
            result = string.split("/")
            day = re.split('-', result[2])
            hours = re.findall(r'\d+', day[3])
            timestamp = day[0] + day[1] + day[2] + hours[0] + hours[1] + "00"
            if timestamp not in timestamp_processed:
                folder = mypath + "/" + result[2] + "/"
                if "index" not in file_name:
                    result = string.split("/")
                    index_path =  '/'.join(result[0:len(result)-1]) + '/index.htm'
                    subprocess.run(["mv", file_name, index_path])
                subprocess.run(["warcit", "--fixed-dt", timestamp, URL_Main, folder])
                timestamp_processed.append(timestamp)


###Weblogs collection

###Problems:

##Files without utf-8 names
#The following list need to be run on bash due to problems with the enconding (i.e., windows)
#list_encodings = ['2rosas.weblog.com.pt', 'a-evolucao-de-darwin.weblog.com.pt', 'abnoxio.weblog.com.pt', 'abracadabra.weblog.com.pt', 'alandroal.weblog.com.pt', 'amnesia.weblog.com.pt', 'anomalias.weblog.com.pt', 'ante-et-post.weblog.com.pt', 'anuariodofutebol.weblog.com.pt', 'apenasmaisum.weblog.com.pt', 'atuleirus.weblog.com.pt', 'bde.weblog.com.pt', 'bloguedeumaloura.weblog.com.pt', 'bloquisto.weblog.com.pt', 'cami.weblog.com.pt', 'charquinho.weblog.com.pt', 'cidadaodomundo.weblog.com.pt', 'claudia.weblog.com.pt', 'contanatura-hemeroteca.weblog.com.pt', 'culinaria.weblog.com.pt', 'devagares.weblog.com.pt', 'enresinados.weblog.com.pt', 'enxoval.weblog.com.pt', 'estudossobrecomunismo.weblog.com.pt', 'feedback.weblog.com.pt', 'feiticeiradasaguasagradas.weblog.com.pt', 'fumacas.weblog.com.pt', 'hollywood.weblog.com.pt', 'jq.weblog.com.pt', 'loucuraenata.weblog.com.pt', 'loud.weblog.com.pt', 'lua.weblog.com.pt', 'luzdosdias.weblog.com.pt', 'maquinaespeculativa.weblog.com.pt', 'maschamba.weblog.com.pt', 'meuslivros.weblog.com.pt', 'movcineclubes.weblog.com.pt', 'mulher50a60.weblog.com.pt', 'nascouves.weblog.com.pt', 'navegologoexisto.weblog.com.pt', 'no-mundo.weblog.com.pt', 'o-planeta-diario.weblog.com.pt', 'observador.weblog.com.pt', 'outsider.weblog.com.pt', 'papagaioazul.weblog.com.pt', 'patatapatati.weblog.com.pt', 'planicie-heroica.weblog.com.pt', 'populo.weblog.com.pt', 'proverbios.weblog.com.pt', 'prusidente.weblog.com.pt', 'putadevida.weblog.com.pt', 'quem-me-dera-que-fosse-sempre-penalty.weblog.com.pt', 'queremama.weblog.com.pt', 'queuniversidade.weblog.com.pt', 'renaseveados.weblog.com.pt', 'santosdacasa.weblog.com.pt', 'sd.weblog.com.pt', 'semiramis.weblog.com.pt', 'setubalarqblog2.weblog.com.pt', 'spectrum.weblog.com.pt', 'terceiroanel.weblog.com.pt', 'terraviva.weblog.com.pt', 'troll-urbano.weblog.com.pt', 'u2only.weblog.com.pt', 'vistasnapaisagem.weblog.com.pt', 'vivarte.weblog.com.pt', 'whitetiger.weblog.com.pt', 'xafarica.weblog.com.pt']

##We assume that index.html is the root
##The timestamp used is the same reported by the author (between 01/01/2012 - 31/12/2012)

#To extract the files with problems on encondings
#list_folders_not_processed = []

mypath = "./weblogs"
bash = True #The script is running on bash?
file_name_processed = []
for subdir, dirs, files in os.walk(mypath):
    for file in files:
        file_name = os.path.join(subdir, file)
        result = file_name.split("/")
        #try:
            ##Check if there is problems with enconding
            #text = file_name.encode("utf-8")
        #except:
            #list_folders_not_processed.append(result[2])
        if "index" in file_name and result[2] not in file_name_processed:
            folder = mypath + "/" + result[2] + "/"
            URL_Main = "http://www." + result[2] + "/"
            if bash:
                subprocess.run(["warcit", "--charset", "ISO-8859-1", "--fixed-dt", "20121231245959", URL_Main, folder])
            else:
                subprocess.run(["warcit", "--fixed-dt", "20121231235959", URL_Main, folder])
            file_name_processed.append(result[2])


###DEM-IST

###Problems:
## To define the timestamp all the root folders need to have the year of each version. For instance, "site-DEM-old-mac-1996-1997" --> "site-DEM-old-mac-1998".
## Then, for each folder, we will see what is the biggest timestamp in the year referenced before.
## Due to the especification of the author in the folder "site-IDMEC-old-mac-1998" the file "IDMEC.HTML" need to be "idemc.htm"
## Confusion between the name "DEM" and "IDEM". So, I change "IDEM" --> "Eng" (problems with warcit)

mypath = "./DEM-IST"
dic_URLs = {"site-DEM-2001": "http://www.dem.ist.utl.pt/", "site-DEM-2006": "http://www.dem.ist.utl.pt/", "site-DEM-2007": "http://www.dem.ist.utl.pt/", "site-DEM-old-mac-1998": "http://lemac18.lemac.ist.utl.pt/DEM/", "site-IDMEC-old-mac-1998": "http://lemac18.lemac.ist.utl.pt/IDMEC/", "site-SPM-2006-promec": "http://www.dem.ist.utl.pt/~spm/", "site-SPM-old-2004": "http://www.dem.ist.utl.pt/~spm/"}
file_name_processed = []
primeira_vez = True
for subdir, dirs, files in os.walk(mypath):
    if primeira_vez:
        primeira_vez = False
        continue
    else:
        for file in files:
            file_name = os.path.join(subdir, file)
            string = os.path.join(subdir, file) 
            result = string.split("/")
            if result[2] not in file_name_processed:
                try:
                    lis = []
                    date_from_folder = ''.join(list(filter(str.isdigit, result[2])))
                    for subdir, dirs, files in os.walk(subdir):
                        for file in files:
                            file_name = os.path.join(subdir, file)
                            recovery_date = os.stat(file_name).st_mtime
                            timestamp = datetime.utcfromtimestamp(recovery_date).strftime('%Y%m%d%H%M%S')
                            date = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
                            if date_from_folder in str(date.year):
                                lis.append(timestamp)
                    min_date = max(lis)
                    folder = mypath + "/" + result[2] + "/"
                    if result[2] == "site-DEM-old-mac-1998": 
                        import pdb;pdb.set_trace()
                        ##Do not work
                        ##Only with the command: warcit --index-files DEM.HTML --fixed-dt 19981030112146 http://lemac18.lemac.ist.utl.pt/DEM/ ./DEM-IST/site-DEM-old-mac-1998/
                        continue
                    else:
                        subprocess.run(["warcit", "--fixed-dt", min_date, dic_URLs[result[2]], folder])
                    file_name_processed.append(result[2])
                except:
                    print("Error, Explore with trace()")
                    import pdb;pdb.set_trace()

###Move all WARC files to another folder
list_warcs_to_move = glob.glob("./*.warc.gz")
subprocess.run(["mkdir", "warcs"])
for file_name in list_warcs_to_move:
    result = file_name.split("/")
    index_path = "./warcs/" + result[1]
    subprocess.run(["mv", file_name, index_path])