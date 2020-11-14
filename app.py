try:
    import selenium
    import logging
    import os
    import time
    import sys
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import NoAlertPresentException
    import pandas as pd
    from bs4 import BeautifulSoup
    from webdriver_manager.chrome import ChromeDriverManager
    from mailing import *
    from enum import Enum
    from io import BytesIO, StringIO
    from typing import Union
    import pandas as pd
    import streamlit as st
    #from internshala import *
    import pandas as pd
except Exception as e:
    print(e)
 
STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""
log_file_path = "naukri.log"
logging.basicConfig(
    level=logging.INFO, filename=log_file_path, format="%(asctime)s    : %(message)s"
)
# logging.disable(logging.CRITICAL)
os.environ["WDM_LOG_LEVEL"] = "0"
options = webdriver.ChromeOptions()
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")  # ("--kiosk") for MAC
options.add_argument("--disable-popups")
options.add_argument("--disable-gpu")
a=False

def log_msg(message):
    """Print to console and store to Log"""
    print(message)
    logging.info(message)


def catch(error):
    """Method to catch errors and log error details"""
    exc_type, exc_obj, exc_tb = sys.exc_info()
    lineNo = str(exc_tb.tb_lineno)
    msg = "%s : %s at Line %s." % (type(error), error, lineNo)
    print(msg)
    logging.error(msg)

def is_element_present(driver, how, what):
    """Returns True if element is present"""
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True

def GetElement(driver, elementTag, locator="ID"):
    """Wait max 15 secs for element and then select when it is available"""
    try:
        if locator == "ID":
            if is_element_present(driver, By.ID, elementTag):
                return WebDriverWait(driver, 15).until(
                    lambda driver: driver.find_element_by_id(elementTag)
                )
            else:
                log_msg("%s Not Found." % elementTag)
                return None

        elif locator == "NAME":
            if is_element_present(driver, By.NAME, elementTag):
                return WebDriverWait(driver, 15).until(
                    lambda driver: driver.find_element_by_name(elementTag)
                )
            else:
                log_msg("%s Not Found." % elementTag)
                return None

        elif locator == "XPATH":
            if is_element_present(driver, By.XPATH, elementTag):
                return WebDriverWait(driver, 15).until(
                    lambda driver: driver.find_element_by_xpath(elementTag)
                )
            else:
                log_msg("%s Not Found." % elementTag)
                return None

        elif locator == "CSS":
            if is_element_present(driver, By.CSS_SELECTOR, elementTag):
                return WebDriverWait(driver, 15).until(
                    lambda driver: driver.find_element_by_css_selector(elementTag)
                )
            else:
                log_msg("%s Not Found." % elementTag)
                return None

    except Exception as e:
        catch(e)
    return None

def WaitTillElementPresent(driver, elementTag, locator="ID", timeout=30):
    """Wait till element present. Default 30 seconds"""
    result = False
    driver.implicitly_wait(0)
    for i in range(timeout):
        try:
            if locator == "ID":
                if is_element_present(driver, By.ID, elementTag):
                    result = True
                    break
            elif locator == "NAME":
                if is_element_present(driver, By.NAME, elementTag):
                    result = True
                    break
            elif locator == "XPATH":
                if is_element_present(driver, By.XPATH, elementTag):
                    result = True
                    break
            elif locator == "CSS":
                if is_element_present(driver, By.CSS_SELECTORS, elementTag):
                    result = True
                    break
        except Exception as e:
            log_msg("Exception when WaitTillElementPresent : %s" % e)
            pass
        time.sleep(0.99)
    else:
        log_msg("Timed out. Element not found: %s" % elementTag)
    driver.implicitly_wait(3)
    return result

#df=pd.DataFrame()
class FileUpload(object):
 
    def __init__(self):
        self.fileTypes = ["csv"]
 
    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        # st.info(__doc__)
        # st.markdown(STYLE, unsafe_allow_html=True)
        st.header("Internshala Crawler")
        global username 
        user= st.text_input("Username of Internshala:",key="username")
        username=user
        global password 
        password= st.text_input("Password of Internshala:",type="password",key="pass")
        file = st.file_uploader("Upload file", type=self.fileTypes,key="file_uplode")
        show_file = st.empty()
        if st.button('Submit'):
            global a
            a=True
        #print(a)
        if not file:
            show_file.info("Please upload a file of type: " + ", ".join(["csv"]))
            return
        content = file.getvalue()
        df=pd.DataFrame()
        
        if isinstance(file, BytesIO):
            show_file.image(file)
        else:
            df = pd.read_csv(file)
            st.dataframe(df)

        return df
            
def login(df,headless = False):
    #username = "theprofessor.tle.99@gmail.com"
    #password = "naukriportal"
    mob = "1234567890"  # Type your mobile number here
    URL = "https://internshala.com/"
    driver = webdriver.Chrome(
    executable_path=ChromeDriverManager().install(), chrome_options=options
    )
    driver.get(URL)

    if "internshala" in driver.title.lower():
        print("Website Loaded Successfully.")

    if is_element_present(driver, By.CLASS_NAME, "home_page_login_button"):
        ll=driver.find_element_by_css_selector('button.home_page_login_button')   
        ll.click()
        time.sleep(2)
    
    if is_element_present(driver, By.ID, "modal_email"):
        emailFieldElement = GetElement(driver, "modal_email", locator="ID")
        emailFieldElement.clear()
        emailFieldElement.send_keys(username)
        time.sleep(1)
        passFieldElement = GetElement(driver, "modal_password", locator="ID")
        passFieldElement.clear()
        passFieldElement.send_keys(password)
        time.sleep(1)
        final_login=GetElement(driver, "modal_login_submit", locator="ID")
        final_login.click()
        #loginXpath = '//*[@type="submit"]'
        #loginButton = driver.find_element_by_xpath(loginXpath)
        time.sleep(2)
    lt=list()
    for link in df['job_link']:
        try:
            if link==" " or link==None:
                continue
            driver.get(link)

            time.sleep(3)
            try:
                l=driver.find_element_by_link_text("Apply now")
                l.click()
                time.sleep(1)
            except:
                lt.append('Already applied OR applications are closed')
                print("Already applied OR applications are closed")
                continue
            ll=driver.find_element_by_css_selector('button.education_incomplete')   
            ll.click()
            #time.sleep(3)


            txtarea1Xpath="//textarea[@id='cover_letter']"
            WaitTillElementPresent(driver, txtarea1Xpath, locator="XPATH", timeout=30)
            textFieldElement = GetElement(driver, txtarea1Xpath, locator="XPATH")
            textFieldElement.send_keys('I have done couples of projects in same skills that you wanted. I am team player and complete project within deadline.')
            
            
            txtarea2Xpath="//*[@placeholder='e.g. I am available full time in Pune for the next 6 months, but will have exams for 15 days in June.']"
            textFieldElement2 = GetElement(driver, txtarea2Xpath, locator="XPATH")
            textFieldElement2.send_keys('I am available for complete interval for internship at desired location')
            
            #try:
            #temp=txtarea2Xpath="//*[@placeholder='e.g. I am available full time in Pune for the next 6 months, but will have exams for 15 days in June.']"
            
            submitXpath="//input[@id='submit'][@value='Submit']"
            SubmitField = GetElement(driver, submitXpath, locator="XPATH")
            SubmitField.click()
            goback="//*[@id='backToInternshipsCta']"
            BackField=GetElement(driver, goback, locator="XPATH")
            try:
                BackField.click()
                lt.append("Applied")
                print("Applied!!")
            except:
                textFieldElement.clear()
                textFieldElement2.clear()
                driver.refresh()
                lt.append("More than 2 questions asked")
                time.sleep(1)
                driver.switch_to.alert.accept()
                time.sleep(1)
        except:
            lt.append('skipped link due to slow loading')
            print("skipped link due to slow loading = ",link)
            time.sleep(1)
    
    driver.close()
    print(" ")
    df['result']=lt
    df.to_csv("result1.csv")
    for i in lt:
        print(i)
if __name__ ==  "__main__":
    helper = FileUpload()
    #df=pd.read_csv(r'C:\Users\Singla\Desktop\learning folder\seleneium\second_data.csv')
    df=helper.run()
    #df=pd.read_csv(r'C:\Users\Singla\Desktop\learning folder\seleneium\second_data.csv')
    #print(a)
    if a==True:
        login(df)

    
    
    
    
