## technorelay test

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pprint import pprint
from selenium.webdriver.common.keys import Keys

testLogin = ""
testPwd = ""

# test data class
class elem:
    def __init__(self, field, type, locator_type, locator_value, value):
        self.field = field
        self.type = type
        self.locator_type = locator_type
        self.locator_value = locator_value
        self.value = value

# test data
fields = [
    elem("username", "input", "name", "username", "user12345"), #can be generated
    elem("email", "input", "name", "email", "u@gmail.com"), #can be generated
    elem("title", "select", "name", "title", "0"),
    elem("first name", "input", "name", "firstName", "John"),
    elem("last name", "input", "name", "lastName", "Doe"),
    elem("password", "input", "name", "password", "Usr12345678!"),
    elem("confirm password", "input", "name", "confirmPassword", "Usr12345678!"),
    elem("Clinic IDs", "search", "xpath", "/html/body/div/div[1]/div/div/form/div[5]/div[1]/div/div/div/div[1]/input", "0"),
    elem("National Provider ID", "input", "name", "npi", "123"),
    elem("Residence", "input", "name", "doctorResidency", "residency01"),
    elem("Specialities", "button", "xpath", "/html/body/div/div[1]/div/div/form/div[8]/div[1]/button", "SPEC"),
    elem("Medical licenses", "button", "xpath", "/html/body/div/div[1]/div/div/form/div[8]/div[2]/button", "LIC"),
    elem("Degree", "input", "name", "doctorDegree", "1"),
    elem("date of birth", "input", "name", "dateOfBirth", "06/19/1970"), # MM/DD/YYYY
    elem("gender", "radio", "name", "gender", "0"),
    elem("Phone: Contact phone type", "select", "name", "numberType", "0"),
    elem("Phone: Country code", "select", "name", "countryCode", "0"),
    elem("Phone: number", "input", "name", "phoneNumber", "0671234567"),
    elem("Address: Country", "select", "name", "country", "0"),
    elem("Address: State", "select", "name", "state", "0"),
    elem("Address: ZIP", "input", "name", "zipCode", "99876"),
    elem("Address: Street", "input", "name", "street", "Elm street 1428"),
    elem("Address: City", "input", "name", "city", "Springwood"),
    elem("Communication modes", "checkbox", "name", "communicationModes", "0"),
    elem("Payment modes", "radio", "name", "paymentMode", "0"),
    elem("Permissions", "checkbox", "name", "permissions", "0"),
    elem("Fee", "input", "name", "fee", "1")

]

# special type of data need special processing
Spec = "Therapist"
Spec_connector = "doctorSpeciality"
add_spec = "/html/body/div/div[1]/div/div/form/form/div[2]/button"

Lic_text = "ABCDE12345"
add_lic = "/html/body/div/div[1]/div/div/form/form/div[2]/button"

#### end of test data ####


# start
#pprint("Start.")

# Open browser
driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://"+testLogin+":"+testPwd+"@Abc@test-qa.technorely.com/admin/create-provider")
# direct link could not be open for some reason (mb bug)

# log in
e = driver.find_element_by_css_selector(".form > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)")
e.send_keys(testLogin)
e = driver.find_element_by_css_selector(".form > form:nth-child(1) > div:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)")
e.send_keys(testPwd)
e = driver.find_element_by_css_selector("button.content-wrapper-blue_link")
e.click()

#go to "create provider" form
wait = WebDriverWait(driver,10)
e = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"li.sidebar-nav_item:nth-child(4) > a:nth-child(1) > span:nth-child(2)")))
e.click()


wait = WebDriverWait(driver, 5)

# process fields from test data
for f in fields:
    try:
        if f.type == "input":
            if f.locator_type == "name":
                e = wait.until(EC.element_to_be_clickable((By.NAME, f.locator_value)))
                #pprint("field input: "+f.field)
                #e = driver.find_element_by_name(f.locator_value)
                e.send_keys(f.value)
        elif f.type == "select":
            if f.locator_type == "name":
                e = wait.until(EC.element_to_be_clickable((By.NAME, f.locator_value)))
                #pprint("field selector: "+f.field)
                e = Select(driver.find_element_by_name(f.locator_value))
                e.select_by_index(int(f.value))
        elif f.type == "radio" or f.type == "checkbox":
            if f.locator_type == "name":
                e = wait.until(EC.presence_of_all_elements_located((By.NAME, f.locator_value)))
                #e = wait.until(EC.elements _to_be_clickable((By.NAME, f.locator_value)))
                e = driver.find_elements_by_name(f.locator_value)
                #e[0].click()
                driver.execute_script("arguments[0].click();", e[0])
        elif f.type == "search":
            if f.locator_type == "xpath":
                e = wait.until(EC.element_to_be_clickable((By.XPATH, f.locator_value)))
                #e = driver.find_elements_by_name(f.locator_value)
                e.click()
                e.send_keys(Keys.RETURN)
        elif f.type == "button":
            #to avoid interaction of spec & lic forms
            driver.implicitly_wait(5)
            if f.locator_type == "xpath":
                e = wait.until(EC.element_to_be_clickable((By.XPATH, f.locator_value)))
                e.click()
                if f.value == "SPEC":
                    e = wait.until(EC.element_to_be_clickable((By.NAME, Spec_connector)))
                    e.send_keys(Spec)

                    #add
                    e = driver.find_element_by_xpath(add_spec).click()
                elif f.value == "LIC":
                    #country
                    e = wait.until(EC.presence_of_all_elements_located((By.NAME, "country")))
                    e = Select(e[0])
                    e.select_by_index(0)

                    #state
                    e = wait.until(EC.presence_of_all_elements_located((By.NAME, "state")))
                    e = Select(e[0])
                    e.select_by_index(0)

                    #License text
                    e = driver.find_element_by_name("licence") #misprint
                    e.send_keys(Lic_text)

                    #License date
                    e = driver.find_element_by_name("date")
                    e.click()
                    d = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/div/form/form/div[1]/div[4]/fieldset/div/div/div[2]/div/span[16]")))
                    d.click()

                    #add
                    e = driver.find_element_by_xpath(add_lic).click()

    except:
        pprint("ERROR: "+f.field)
        raise

#timeout to observe the result!
driver.implicitly_wait(10)

#SUBMIT new provider
driver.find_element_by_xpath("/html/body/div/div[1]/div/div/form/div[21]/div/button[2]").click()

#timeout to observe the result!
driver.implicitly_wait(10)

driver.close()

#done :D
#pprint("Done.")