from selenium import webdriver
import configparser
import subprocess
import os 

driver_options=webdriver.ChromeOptions()
driver_options.add_experimental_option("detach",True)
driver=webdriver.Chrome(options=driver_options)
driver.maximize_window()

driver.get("https://triserv360.com/")
    
def load_time(end_time,start_time):
    time_secs=(end_time-start_time)/1000
    return time_secs

html_table="<html><head>Website load time</head><body><table border=1><tr><th>Page Name</th><th>Backend Time</th><th>Frontend Time</th></tr>"

config_data=configparser.ConfigParser()
config_data.read("urls.ini")
nav_bar=config_data["Navigation_bar"]

for nav in nav_bar:
    driver.get(nav_bar.get(nav))
    navigationStart = driver.execute_script('return window.performance.timing.navigationStart')
    responseStart = driver.execute_script('return window.performance.timing.responseStart')
    loadEventEnd = driver.execute_script('return window.performance.timing.loadEventEnd')
    #backendtime=resposeStart-navigationStart
    backend_time=load_time(responseStart,navigationStart)
    #frontendtime=loadEventEnd-responseStart
    frontend_time=load_time(loadEventEnd,responseStart)
    html_table+=f'<tr><td><a href="{nav_bar.get(nav)}" target="_blank">{nav}</a></td><td>{backend_time}</td><td>{frontend_time}</td></tr>'

html_table+="</table></body></html>"

file_name="websiteloadtime.html"

with open(file_name,"w") as file:
    file.write(html_table)

driver.quit()

script_directory = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(script_directory, file_name)
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

subprocess.Popen([chrome_path, html_file_path])