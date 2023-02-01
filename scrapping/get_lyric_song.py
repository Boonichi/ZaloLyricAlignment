from ..libs import*


url='https://www.nhaccuatui.com/tim-kiem?q={}'
download_dic='Download'

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
  "download.default_directory": download_dic,
  "download.prompt_for_download": False,
})

chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=chrome_options)

driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dic}}
command_result = driver.execute("send_command", params)



def latest_download_file(path):
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    return newest



def check_is_lyricline(line):
    if ('ver' in line or 'verse' in line or 'chorus' in line or 'outro' in line or 'kết' in line or 'bài hát:' in line or 'song:' in line or '[' in line or ']' in line):
        return False
    return True

def preprocessing_name(name):
    name    =unidecode(name)
    
    names   =name.split(' ')
    name    =''
    for element in names:
        if(element!=""):
            name+=element+" "
    
    name    =name[:-1]
    name    =name.replace(' ','+')
    return name


def processing_lyric(lyric):
    lyric=lyric.lower()
    lyric=lyric.replace(','," ")
    lyric=lyric.replace('.'," ")
    lyric=lyric.replace('/'," ")
    lyric=lyric.replace('?'," ")
    lyrics=lyric.split('\n')
    correct_lyric=[]
    flag=0
    for line in lyrics:
        if (check_is_lyricline(line)):
            for element in line.split(' '):
                if(element!=''):
                    if(len(element)==1):
                        if(flag==1):
                            correct_lyric[-1]=correct_lyric[-1]+element
                        else:
                            correct_lyric.append(element)
                            flag=1
                    else:
                        correct_lyric.append(element)
                        flag=0
    return correct_lyric

def take_lyric_song(name):
    driver.get(url.format(preprocessing_name(name))) 
    sleep(random.randint(3,5))
    
    link_song=driver.find_elements(By.CSS_SELECTOR,'.sn_search_single_song a')[0].get_attribute('href')
    
    driver.get(link_song)
    
    sleep(random.randint(3,5))
    #get lyric
    lyric=driver.find_element(By.CSS_SELECTOR,'.pd_lyric').text
    lyric=processing_lyric(lyric)
    
    download_button=driver.find_element(By.CSS_SELECTOR,'#btnDownloadBox')
    download_button.click()
    sleep(10)
    button_128KB=driver.find_element(By.CSS_SELECTOR,'#downloadBasic')
    button_128KB.click()
    sleep(10) # to downloading
    
    driver.quit()
    
    path=latest_download_file(download_dic)
    # need to store the file and rename it
    return lyric,os.path.join(download_dic,path)

    
    