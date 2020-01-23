from requests_html import HTML, HTMLSession
import requests
from lxml import html
from pathlib import Path
from os import mkdir



# crawler function will loop trough all pages and will get the links to the lessons that we are trying to download
def crawler(max_pages):
    page = 1 # starting page

    while page <= max_pages:
        url = f'https://www.activemelody.com/lessons/?sf_paged={page}' 
        lessons_page = session.get(url)
        lessons_container = lessons_page.html.find('.lessons-container') # Gets the container that lessons are in


        for link in lessons_container: # Loops trough all lessons and gets theyr links
            get_lessson_link = link.find('h3 a', first=True).attrs['href'] 
            open_link(get_lessson_link) 

        page += 1 



# This function will open each lesson link
# And will create a folder with the lesson name on our machine
def open_link(lesson_link):

    try:
        
        get_lesson = session.get(lesson_link)
        links = get_lesson.html.find('.one-third', first=True).absolute_links
        title = get_lesson.html.find('h1', first=True).text 
        folder_name = title[-5:] )

        folder = mkdir(f'/media/corvuses/F458599B58595E04/BACKING_TRACKS/Active Melody/{folder_name}')


        for link in links:
            file_name = link.rsplit('/',1)[1]
            download_pdf(link, file_name, folder_name)

    except Exception as e:
        print('Something Went Wrong')



# After a lessons is opened this function will download the actual lesson
# And save it in the right folder
def download_content(link, file_name, folder):

    response = session.get(link)

    content = Path(f'/media/corvuses/F458599B58595E04/BACKING_TRACKS/Active Melody/{folder}/{file_name}')
    content.write_bytes(response.content)

    print(f'{link} Downloaded!')



# IMPORTANT check if the site wants CSRF token and provide it here or else you wont be abe to login
with HTMLSession() as session:
    url = 'https://www.activemelody.com/wp-login.php?wpe-login=true'
    log = ''
    pwd = ''

    session.get(url)
    
    login_data = dict(log=log, pwd=pwd)
    session.post(url, data=login_data)

    crawler(19)