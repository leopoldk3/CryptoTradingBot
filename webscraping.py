from selenium import webdriver

browser = webdriver.Chrome("/Users/leoklotz/Desktop/projects/CryptoTradingBot/chromedriver")

url = "https://coinmarketcap.com/gainers-losers/"

browser.get(url)


#xpath to the currency link goes here 
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr[1]/td[2]/a').click()


#Right now this takes the top spot of coinmarket cap's top gainers and losers (top 100 is not specified) and opens up the top currency's coinmarketcap webpage
