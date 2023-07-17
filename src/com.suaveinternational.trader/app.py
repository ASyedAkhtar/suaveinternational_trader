import yfinance as yf

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def get_current_price(instrument):
    data = yf.Ticker(instrument).info["currentPrice"]
    return data

def get_window(instrument, period, interval, num_intervals):
    data = yf.Ticker(instrument).history(period=period, interval=interval)
    recentData = data.iloc[-num_intervals:]
    return recentData

def get_window_drop_price(instrument, period, interval, num_intervals):
    data = yf.Ticker(instrument).history(period=period, interval=interval)
    recentData = data.iloc[-num_intervals:]
    recentCloseData = recentData[["Close"]]
    recentCloseDeltaData = recentCloseData.diff().rename(columns={"Close": "Delta"})
    recentCloseDropData = recentCloseDeltaData[recentCloseDeltaData["Delta"] < 0].rename(columns={"Delta": "Drop"})
    return recentCloseDropData.mean()

def test_selenium():
    driver = webdriver.Firefox()
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element(By.NAME, "q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()

#print(get_current_price("MSFT"))
# Test if the Open or Close are blank in the middle of a trading day.
trade_window = get_window("AMD", "1d", "1m", 30)
# Get average price drop in a window of trading.
average_drop = get_window_drop_price("AMD", "1d", "1m", 30)
print(trade_window)
print(average_drop)
