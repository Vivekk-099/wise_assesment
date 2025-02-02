from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver,4)
action = ActionChains(driver)
driver.get("https://staging-web.wise.live")
driver.maximize_window()
# Scenario 1 : Perform login as tutor

wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='text--16 height-48 primary--text v-btn v-btn--block v-btn--has-bg theme--light v-size--default large secondary-bg ']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='vti__dropdown']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='+91']"))).click()
wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Phone number']"))).send_keys("1111100000")
driver.find_element(By.XPATH,"//span[normalize-space()='Get OTP']").click()
wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@autocomplete='one-time-code']")))
otp_Input_field=driver.find_elements(By.XPATH,"//input[@autocomplete='one-time-code']")
otp = '0000'
for i in range(4):
    otp_Input_field[i].send_keys(otp[i])

driver.find_element(By.XPATH, "//button[@class='mt-6 v-btn v-btn--block v-btn--has-bg theme--light v-size--default large primary-bg ']").click()
institute_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='institute-title ml-2 cursor font-weight--600 text--16']"))) 
assert "Testing Institute" in institute_name.text, "Institute name not found!"
print("Login successful and 'Testing Institute' is displayed.")

#Scenario 2 : Go To The Classroom

driver.find_element(By.XPATH,"//span[normalize-space()='Group courses']").click() 
time.sleep(2)
wait.until(EC.element_to_be_clickable((By.LINK_TEXT,"Classroom for Automated testing"))).click()
classroom_name = wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='text--24 font-weight--600']")))
assert "Classroom for Automated testing" in classroom_name.text, "Classroom name not found!"
print("Classroom is opened successfully and 'Classroom for Automated testing' is displayed.")
time.sleep(1)

#Scenario 3 : Schedule a Session

wait.until(EC.element_to_be_clickable((By.LINK_TEXT,"Live Sessions"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Schedule Sessions']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='ml-2 text--16 truncate']")))
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Add session']"))).click()
time.sleep(7)
wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='text--16 text-center'])[1]"))).click()
selected_year = wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='v-picker__title__btn v-date-picker-title__year']"))).text
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='v-btn v-date-picker-table__current v-btn--active v-btn--text v-btn--rounded theme--light primary']"))).click()
selected_date=driver.find_element(By.XPATH,"(//div[@class='text--16 text-center'])[1]").text
time.sleep(1)
wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@role='combobox']"))).click()
selected_time=driver.find_element(By.XPATH,"/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[10]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/input[1]")
selected_time.clear()
selected_time.send_keys("11:45")
scheduled_date_time = selected_date[5:11] + ' ' + selected_year[2:5]+'11:45 PM'
actions = ActionChains(driver) 
actions.send_keys(Keys.ENTER)
actions.perform()
time.sleep(1)
scheduled_time = driver.find_element(By.XPATH,"//div[@class='text--16']")
if scheduled_time.text == "AM" :
   scheduled_time.click()
driver.find_element(By.XPATH,"//button[contains(@class,'v-btn v-btn--has-bg theme--light v-size--default medium primary-bg')]").click()
time.sleep(1)

#Scenario 4 : Assert the session

timeline_card_List = driver.find_elements(By.XPATH,"//div[@class='d-flex align-center flex-wrap mt-1 text--12 greySecondary--text font-weight--500']")
session_Detail=driver.find_elements(By.XPATH,"//div[@class='text--18 font-weight--600 mb-2']")
Instructor_name=driver.find_elements(By.XPATH,"//div[@class='heading py-10 px-4 px-sm-6']//div[2]")
upcoming_Status=driver.find_elements(By.XPATH,"//div[@class='px-4 py-3 px-sm-6']//div[@class='d-flex align-center justify-space-between']//div[@class='d-flex align-center']//div//span[@class='v-chip__content']")
for i in range(len(timeline_card_List)):
    selected_date_time = timeline_card_List[i].text[0:9] + timeline_card_List[i].text[10:18]
    Duration = timeline_card_List[i].text[19:25]
    if(selected_date_time==scheduled_date_time):
        assert "02 Feb 2511:45 PM" in selected_date_time,"Session Card not Shown"
        print("Session card for scheduled date can be seen on timeline")
        SessionDetails=session_Detail[i].text
        InstructorName=Instructor_name[i].text
        UpcomingStatus=upcoming_Status[i].text
        break

assert "Live session" in SessionDetails,"Session Name Incorrect"
print("Session Name : " + SessionDetails)
assert "Wise Tester" in InstructorName,"Instructor Name Incorrect"
print("Instructor : " + InstructorName[1:])
assert "Upcoming" in UpcomingStatus,"Upcoming Status Incorrect"
print("Status : " + UpcomingStatus)
assert "60 min" in Duration,"Duration not correct"
print("Duration : " + Duration) 