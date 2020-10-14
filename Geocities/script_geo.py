import os
from datetime import datetime
import subprocess
import os.path
import multiprocessing
import click
import glob

#import pdb;pdb.set_trace()

def extract_content(folder):
    """
    Extract information from 7zips
    """

    ##1.  7Zip files

    mypath = "./" + folder
    for subdir, dirs, files in os.walk(mypath):
        for file in files:
            if file.endswith(".001"):
                file_name = os.path.join(subdir, file)
                os.system("7za x " +  file_name + " -o" + folder + "/")

    ##2.  Add extension ".tar" (The files are TARs but do not have extension)

    mypath = "./" + folder
    for subdir, dirs, files in os.walk(mypath):
        for file in files:
            if not file.endswith(".tar"):
                file_name = os.path.join(subdir, file)
                os.system("mv " +  file_name + " " + file_name + ".tar")
    
    ##3.  Extract TAR

    for subdir, dirs, files in os.walk(mypath):
        for file in files:
            if file.endswith(".tar"):
                file_name = os.path.join(subdir, file)
                os.system("tar -xvf " +  file_name)


def get_timestamp(file_name):
    """
    Get timestamp from the file that will be used do generate the correct WARC record 
    (i.e., we use the timestamp from the file and we assume that was when it was saved/stored)
    """    
    recovery_date = os.stat(file_name).st_mtime
    timestamp = datetime.utcfromtimestamp(recovery_date).strftime('%Y%m%d%H%M%S')
    if int(timestamp) > 20110000000000:
        return "20091026194848"
    else:
        return timestamp

def process(subdir, elem, main_URL):
    """
    Generate the WARC file using WARCIT. More info: https://github.com/webrecorder/warcit
    """
    file_name = os.path.join(subdir, elem)
    if os.path.isdir(file_name):
        timestamp = get_timestamp(file_name)
        subprocess.run(["warcit", "--fixed-dt", timestamp, main_URL + elem + "/", file_name + "/"])

def generate_WARCS(folder):
    
    ##We assume that for most files the correct url is "www.geocities.com"
    main_URL = "http://www.geocities.com/"
    
    ###Folder Specification:
    ##Most of the folders have the following structure:
    #Folder_Name (e.g., LOWERCASE_FOLDER) -> YAHOOIDS -> Letter or number (e.g., "a" in the case LOWERCASE_FOLDER) -> Letter or number   
    mypath = "./"+ folder +"/YAHOOIDS"
    
    for _, dirs_1, _ in os.walk(mypath):
        with click.progressbar(length=len(dirs_1), show_pos=True) as progress_bar:
            for elem_1 in dirs_1:
                progress_bar.update(1)
                mypath_new_1 = mypath + "/" + elem_1 + "/"
                for _, dirs_2, _ in os.walk(mypath_new_1):              
                    for elem_2 in dirs_2:                    
                        mypath_new_2 = mypath + "/" + elem_1 + "/" + elem_2 + "/"
                        for subdir, dirs, files in os.walk(mypath_new_2):
                            ##In this section we process each folder in parallel
                            p = multiprocessing.Pool()
                            for elem in dirs:
                                p.apply_async(process, [subdir, elem, main_URL])   
                            p.close()
                            p.join()
                            ##Then we move all the WARC files to the corresponding folder
                            for file in glob.glob("*.warc.gz"):
                                ##FIXME, change path
                                os.system("mv " + "/data/collections/Geocities/Files_To_Process/"+ file + " ./WARC_ARCHIVE/") 
                            break #only the top files are processed

def generate_WARCS_subsites(folder):
    """
    This function deals only with the special case of the folder "Subsistes".
    Since, the "main_URL" is different for each folder and the directory structure is different.
    """

    main_URL = "http://"
    mypath = "./"+ folder
    
    for _, dirs_1, _ in os.walk(mypath):
        with click.progressbar(length=len(dirs_1), show_pos=True) as progress_bar:
            for elem_1 in dirs_1:
                progress_bar.update(1)
                mypath_new_1 = mypath + "/" + elem_1 + "/"
                for subdir, dirs, files in os.walk(mypath_new_1):
                    p = multiprocessing.Pool()
                    main_URL += elem_1 + "/" 
                    for elem in dirs:
                        p.apply_async(process, [subdir, elem, main_URL])   
                    p.close()
                    p.join()
                    ##Just to clean the URL
                    main_URL = "http://"
                    for file in glob.glob("*.warc.gz"):
                        ##FIXME, change path
                        os.system("mv " + "/data/collections/Geocities/Files_To_Process/"+ file + " ./WARC_SUBSITES_YAHOO/") 
                    break #only the top files are processed

def generate_WARCS_yahoo(folder):
    
    """
    This function deals only with the special case of the folder "yahoo".
    Since, the "main_URL" is different for each folder and the directory structure is different.
    """

    main_URL = "http://"
    mypath = "./"+ folder
    
    for _, dirs_1, _ in os.walk(mypath):
        with click.progressbar(length=len(dirs_1), show_pos=True) as progress_bar:
            for elem_1 in dirs_1:
                progress_bar.update(1)
                mypath_new_1 = mypath + "/" + elem_1 + "/"
                for subdir_2, dirs_2, _ in os.walk(mypath_new_1):              
                    for elem_2 in dirs_2:                    
                        mypath_new_2 = mypath + "/" + elem_1 + "/" + elem_2 + "/"
                        for subdir, dirs, files in os.walk(mypath_new_2):
                            ##Just to clean the URL
                            main_URL = "http://"
                            if dirs == []:
                                ##If the folder is a file (e.g., the folder "ar.geocities.yahoo.com" only have a index.php file)
                                process(subdir_2, elem_2, main_URL)
                            else:
                                p = multiprocessing.Pool()
                                main_URL += elem_2 + "/" 
                                for elem in dirs:
                                    p.apply_async(process, [subdir, elem, main_URL])   
                                p.close()
                                p.join()       
                            for file in glob.glob("*.warc.gz"):
                                ##FIXME, change path
                                os.system("mv " + "/data/collections/Geocities/Files_To_Process/"+ file + " ./WARC_SUBSITES_YAHOO/") 
                            break #only the top files are processed

if __name__ == '__main__':
    extract_content("YAHOO_FOLDER")
    extract_content("LOWERCASE_FOLDER")
    extract_content("UPPERCASE_FOLDER")
    extract_content("NUMBERS_FOLDER")
    extract_content("SUBSITES_FOLDER")
    generate_WARCS_yahoo("YAHOO_FOLDER")
    generate_WARCS("ARCHIVE_FOLDER")
    generate_WARCS_subsites("SUBSITES_FOLDER")
    generate_WARCS("UPPERCASE_FOLDER")
    generate_WARCS("NUMBERS_FOLDER")
    generate_WARCS("SUBSITES_FOLDER")
    generate_WARCS("UPPERCASE_FOLDER")