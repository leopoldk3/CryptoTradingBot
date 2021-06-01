from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

def get_top_five_gainers(): 
    #creates chromedriver as the driver as long as chromedriver is in the same project folder
    driver = webdriver.Chrome("/Users/leoklotz/Desktop/projects/CryptoTradingBot/chromedriver")
    #sets the URL of the base website I want to workwith
    url = "https://coinmarketcap.com/gainers-losers/"
    #Opens the base website
    driver.get(url)

    #Selects Top 100 and loads that webpage
    #First click on the All timeframes element to open up the dropdown element
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#__next > div > div.main-content > div.sc-57oli2-0.dEqHl.cmc-body-wrapper > div > div.sc-16r8icm-0.xtcyif-0.etwesS > div.sc-16r8icm-0.dOJIkS.table-control-area > div.sc-16r8icm-0.iqcBdR.table-control-action > div.sc-16r8icm-0.tu1guj-0.XdIOT"))).click()
    #Select item "Top 100" from menu dropdown by text found by the xpath
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tippy-9"]/div/div[1]/div/div/button[1]'))).click()

    time.sleep(5)

    # #prints all of the top gainers and their price data (three lines: Title, ticker, (price, gain %, marketcap))
    # tbody = driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/table/tbody')
    # print(tbody.text)

    #puts the top 5 gainer tickers to their respective variables 'gainer_' and then prints the top five out
    gainer1 = str(driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr[1]/td[2]/a/div/div/div').text)
    gainer2 = str(driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr[2]/td[2]/a/div/div/div').text)
    gainer3 = str(driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr[3]/td[2]/a/div/div/div').text)
    gainer4 = str(driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr[4]/td[2]/a/div/div/div').text)
    gainer5 = str(driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr[5]/td[2]/a/div/div/div').text)
    top5 = [gainer1,gainer2,gainer3,gainer4,gainer5]
    #print("The top 5 gaining cryptos at {time_and_date} are: {one}, {two}, {three}, {four}, {five}.".format(time_and_date = str(datetime.datetime.now()), one = gainer1, two = gainer2, three = gainer3, four = gainer4, five = gainer5))
    driver.quit()
    return top5
    
#get_top_five_gainers()