import streamlit as st
from bs4 import BeautifulSoup
import requests
from math import ceil
import time
import csv
import pandas as pd
from gmail import *
from data_prepocess import *
def scrape_main(link):
    response = requests.get(link)
    return(BeautifulSoup(response.text, 'lxml' ))

def app1():
    st.header("Scraper")
    a=st.multiselect('Select field you want to apply for internship',('Computer Science','Marketing','Finance','Mechanical','HR','Civil','Digital Marketing','Electronics','Content Writing'),key='internship_options')
    link={'Computer Science':'https://internshala.com/internships/computer%20science-internship',
    'Marketing':'https://internshala.com/internships/marketing-internship',
    'Finance':'https://internshala.com/internships/finance-internship',
    'Mechanical':'https://internshala.com/internships/mechanical-internship',
    'HR':'https://internshala.com/internships/hr-internship',
    'Civil':'https://internshala.com/internships/civil-internship',
    'Digital Marketing':'https://internshala.com/internships/digital%20marketing-internship',
    'Electronics':'https://internshala.com/internships/electronics-internship',
    'Content Writing':'https://internshala.com/internships/content%20writing-internship'
    }
    email_to=st.text_input('Enter ur Email ID',key="emailID")
    sbtbtn=st.button('Submit')
    if sbtbtn:
        extract(link,a,email_to)
def extract(link,a,email_to):
    links=[]
    for i in a:
        links.append(link[i])
    row_heading = ['source', 'job_link']
    file_name = 'internshala_first_data.csv' 
    file = open(file_name,'w')
    writer = csv.writer(file)
    writer.writerow(row_heading)
    for index,url in enumerate(links):
        soup = scrape_main(url)
        pages = ceil(int(soup.find('div',{'class':'heading heading_4_6'}).text.split()[0])/40)
        for page in range(pages):
            base_url = url + "/page-"+str(page)
            soup1= scrape_main(base_url)
            for single_job in soup.find_all("div", { "class": "individual_internship"}):
                if(single_job.find('div',{'class':'heading_4_5 profile'}) == None):
                    continue
                job_link = "https://internshala.com"
                job_link += single_job.find('div',{'class':'heading_4_5 profile'}).a.get('href')
                source = 'internshala'
                writer.writerow([source, job_link])
    file.close()
    print('file created')
    row_heading = ['source', 'location', 'job_link', 'job_title','company_name', 'imp_fields','description_headings','description','skills','perks']
    file_name = 'internshala_second_raw_data_' + time.strftime("%d_%m_%Y_%H_%M_%S") + ".csv" 
    file = open(file_name,'w', encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(row_heading)
    df = pd.read_csv("internshala_first_data.csv")
    for index,link in enumerate(df.job_link):
        soup = scrape_main(link)
        if soup.find('div',{'class':'heading_4_5 profile'}) == None:
            continue
        
        job_title = soup.find('div',{'class':'heading_4_5 profile'}).text.strip()
        company_name = soup.find('div',{'class':'heading_6 company_name'}).text.strip()
        loc=soup.find('div',{'id':'location_names'}).text.strip()

        imp_fields = []
        for i in soup.find_all('div',{'class':'item_body'}):
            imp_fields.append(i.get_text().strip())
            
        description_headings = []
        for i in soup.find_all('div',{'class':'section_heading heading_5_5'}):
            description_headings.append(i.get_text().strip())
        
        skills=[]
        flag=0
        perks=[]
        for i in (soup.find_all('span',{'class':'round_tabs'})):
            if i.text=='Certificate':
                flag=1
            if flag==0:
                skills.append(i.text)
            else:
                perks.append(i.text)
        
        description = soup.find('div',{'class':'internship_details'}).get_text().strip()
        writer.writerow([df.source[index], loc, df.job_link[index],job_title,company_name, imp_fields,description_headings, description,skills,perks])
    file.close()
    cleaning(file_name)
    mail(email_to,"result1.csv")