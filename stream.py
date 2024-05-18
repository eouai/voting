import os
import json
import time
import tqdm
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nordvpn_switcher import initialize_VPN, rotate_VPN, terminate_VPN

URL = 'http://www.votebowv.com/PacificPoppy'

path = os.path.normpath('C:\\Users\\Burt\\Documents\\Git\\voting\\')
gecko_path = os.path.normpath('C:\\Users\\Burt\\Documents\\Git\\geckodriver\\')
# initialize_VPN(save=1,area_input=['complete rotation'])
initialize_VPN(save=1, area_input=['United States'])
with open(os.path.join(path, 'counts.json'), 'r') as f:
	counts = json.loads(f.read())

with open(os.path.join(path, 'errors.json'), 'r') as f:
	errors = json.loads(f.read())

for i in tqdm.tqdm(range(1,800)):
	try:
		rotate_VPN()
	except Exception as e:
		print(str(e))
		time.sleep(60)

		if errors.get('VPN') is None:
			errors['VPN'] = {'count': 1, str(e): 1}
		else:
			errors['VPN']['count'] += 1
			if errors.get('VPN').get(str(e)) is None:
				errors['VPN'][str(e)] = 1
			else:
				errors['VPN'][str(e)] += 1
		with open(os.path.join(path, 'errors.json'), 'w') as f:
			json.dump(errors, f)

	try:
		browser = webdriver.Firefox(executable_path=os.path.join(gecko_path, 'geckodriver.exe'))
		counts[URL] = counts.get(URL, 0) + 1
		with open(os.path.join(path, 'counts.json'), 'w') as f:
			json.dump(counts, f)
		browser.get(URL)
		time.sleep(5)
		
		element_to_click = browser.find_element(By.XPATH, "//*[@id='nomineeSub_0']")
		browser.execute_script("arguments[0].click();", element_to_click)
		print('Clicking checkbox: "//*[@id=nomineeSub_0]"')
		time.sleep(1)
		element_to_click = browser.find_element(By.XPATH, "//*[@id='nomineeSub_1']")
		browser.execute_script("arguments[0].click();", element_to_click)
		print('Clicking checkbox: "//*[@id=nomineeSub_1]"')
		time.sleep(1)
		element_to_click = browser.find_element(By.XPATH, "//*[@id='nomineeSub_2']")
		browser.execute_script("arguments[0].click();", element_to_click)
		print('Clicking checkbox: "//*[@id=nomineeSub_2]"')
		time.sleep(1)
		element_to_click = browser.find_element(By.XPATH, "//*[@id='nomineeSub_3']")
		browser.execute_script("arguments[0].click();", element_to_click)
		print('Clicking checkbox: "//*[@id=nomineeSub_3]"')
		time.sleep(1)
		element_to_click = browser.find_element(By.XPATH, "//*[@id='nomineeSub_4']")
		browser.execute_script("arguments[0].click();", element_to_click)
		print('Clicking checkbox: "//*[@id=nomineeSub_4]"')
		time.sleep(1)
		
		element_to_click = browser.find_element(By.XPATH, "//*[@id='submitBallotButton']")
		browser.execute_script("arguments[0].click();", element_to_click)
		print('Clicking Submit....')
		time.sleep(3)
		element_to_click = browser.find_element(By.XPATH, "//*[@id='confirm-delete-ok']")
		browser.execute_script("arguments[0].click();", element_to_click)	
		time.sleep(3)
		browser.delete_all_cookies()
		browser.close()
		
	except Exception as e:
		counts[URL] = counts.get(URL, 0) - 1
		if errors.get(URL) is None:
			errors[URL] = {'count': 1, str(e): 1}
		else:
			errors[URL]['count'] += 1
			if errors.get(URL).get(str(e)) is None:
				errors[URL][str(e)] = 1
			else:
				errors[URL][str(e)] += 1
		with open(os.path.join(path, 'errors.json'), 'w') as f:
			json.dump(errors, f)
		print(str(e))
	sleep_time = random.randint(5,30)
	print('sleeping {} seconds...'.format(sleep_time))
	time.sleep(sleep_time)
	try:
		browser.delete_all_cookies()
		browser.close()
	except Exception as e:
		if errors.get(URL) is None:
			errors[URL] = {'count': 1, str(e): 1}
		else:
			errors[URL]['count'] += 1
			if errors.get(URL).get(str(e)) is None:
				errors[URL][str(e)] = 1
			else:
				errors[URL][str(e)] += 1
		with open(os.path.join(path, 'errors.json'), 'w') as f:
			json.dump(errors, f)


terminate_VPN()
