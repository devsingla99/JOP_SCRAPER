import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def remodify(text):
    '''
    A function to extract the skills and not the duplicated skills.
    '''
    a = ''.join([i if((ord(i)>64 and ord(i)<91 ) or (ord(i) >96 and ord(i) <123)) else ' ' for i in text])
    pos = a.find('Learn these skills')
    if(pos>0):
        return(a[:pos].strip())
    else:
        return(a.strip())

def cleaning(file):
    try:
        df2 = pd.read_csv(file)
        start = []
        duration = []
        stipend = []
        last_date = []
        job_mode = []
        for a in df2.imp_fields:
            a = a.replace(']','')
            a = a.replace('[','')
            a = a.replace("'",'')
            a = a.replace('"','')
            start.append(a.split(',')[0].strip())
            duration.append(a.split(',')[1].strip())
            stipend.append(a.split(',')[2].strip())
            last_date.append(a.split(',')[3].strip())
            if(len(a.split(','))==5):
                # for locations of jobs/internships there may not be presence of jobs. At that time it throws error.
                job_mode.append(a.split(',')[4].strip())
            else:
                job_mode.append(None)

        df2['start_date'] = start
        df2['duration'] = duration
        df2['stipend'] = stipend
        df2['last_date'] = last_date
        df2['job_mode'] = job_mode
        for i in range(len(df2['start_date'])):
            if( df2['start_date'][i] == 'Starts\\xa0immediatelyImmediately'):
                df2['start_date'][i] = 'immediately'
        df2.sample(5)
        # cleaning the text in headers columns and adding to a list

        headings = []
        for a in df2.description_headings:
            a = a.replace(']','')
            a = a.replace('[','')
            a = a.replace("'",'')
            headings.append(a.split(','))

        # replacing the cleaned text in heading
        df2.description_headings = headings

        # droping the unwanted columns in the dataframe
        try:
            df3 = df2.drop(['Unnamed: 0','imp_fields'],axis = 'columns')
        except:
            df3=df2
        # attempting on single job description to extract skills 
        start_pos = df3.description[0].find('Skill(s) required')
        end_pos =df3.description[0].find('Who can apply')
        #print(df3.description[0][start_pos+17:end_pos].strip())


        skills = []
        for index, text in enumerate(df3.description_headings):
            for i in text:
                if(i==' Skill(s) required'):
                    start_pos = df3.description[index].find('Skill(s) required')
                    end_pos =df3.description[index].find('Who can apply')
                    skills.append(remodify(df3.description[index][start_pos+17:end_pos].strip()))
                    #print(df3.description[index][start_pos+17:end_pos].strip())
                    break
            else:
                #print(None)
                skills.append(None)


        # extracting the no. of openings based on manual pattern
        no_openings = []
        for index, text in enumerate(df3.description_headings):
            for i in text:
                if(i==' Number of openings'):
                    start_pos = df3.description[index].find('Number of openings')
                    end_pos =df3.description[index].find('Apply now')
                    no_openings.append(df3.description[index][start_pos+19:end_pos].strip())
                    #print(df3.description[index][start_pos+19:end_pos].strip())
                    break
            else:
                #print(None)
                no_openings.append(None)

        # adding the skill set to the dataframe
        df3['skills2'] = skills
        print(df3)
        # ploting the bar graph based on its occurances
        st.header('Job Title VS Number of companies demanding these type of jobs')
        df3.job_title.value_counts().plot(kind='barh', figsize=(15,12))
        #plt.show()
        st.pyplot()



        # appending the number of openings to the dataframe
        df3['no_of_openings'] = no_openings
        # extracting months of internship from the duration column
        months_number = []
        for i in df3.duration:
            months_number.append(int(i.split()[0]))
        df3['months_duration'] = months_number
        # visualizing the pie about the number of job posting and its duration
        st.header("Number of internship openings VS its duration")
        plt.pie(df3.months_duration.value_counts(),labels=df3.months_duration.value_counts().index)
        plt.title("months duration summary")
        st.pyplot()

        st.header('Number of companies vs location')
        df3.location.value_counts().plot(kind='bar', figsize=(15,10))
        #plt.show()
        st.pyplot()

        money_month = []
        incentives = []
        for i in df3.stipend:
            #print(i.split('/'))
            #print(len(i.split('/')))
            if(len(i.split('/'))>1):
                money_month.append(i.split('/')[0].strip())
                x = i.split('/')[1].split()[-1].strip()
                if x == 'Incentives' or x == 'incentives':
                    incentives.append('Yes')
                else:
                    incentives.append('No')
            else:
                incentives.append('No')
                money_month.append(None)
        
        # adding extarcted ones to the dataframe
        df3['stipend_month'] = money_month
        df3['incentives'] = incentives
        df3.to_csv('result1.csv',index=False)
        
        head=[]
        for a in df3['skills']:
            a = a.replace(']','')
            a = a.replace('[','')
            a = a.replace("'",',')
            #a=a.replace("\r\n",',')
            #head.append(a.split(','))
            head.append(a)

        ele=[]
        dic={}
        for i in head:
            ele=list(i.split(","))
            for j in ele:
                if j in dic:
                    dic[j]+=1
                else:
                    dic[j]=1

        dic.pop(" ", None)
        dic.pop("", None)
        print(dic)
        keys = dic.keys()
        values = dic.values()
        st.header("Number of Companies Demanding Particular Skills vs Skills")
        labels = []
        sizes = []

        for x, y in dic.items():
            labels.append(x)
            sizes.append(y)

        # Plot
        plt.pie(sizes, labels=labels)

        plt.axis('equal')
        st.pyplot()
    except:
        st.write("High Load")
cleaning("internshala_second_raw_data_16_11_2020_15_11_21.csv")