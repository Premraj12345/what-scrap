from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, request
from time import sleep

app = Flask(__name__)

#service = Service(executable_path='./chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Add any other options you need
chrome_options.add_argument("--no-sandbox")  # Add any other options you need
chrome_options.add_argument("--disable-dev-shm-usage")  # Add any other options you need

# Initialize the Selenium WebDriver and navigate to the webpage
#driver = webdriver.Chrome(service=service,options=chrome_options)  # Adjust based on your preferred browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

driver.get("https://whatsapp.checkleaked.cc/380947100983")  # Specify the URL you want to navigate to

# Wait for the element to be present on the page - to load fully
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div'))
)

@app.route('/')
def index():
    return "</h1>Working<h1>"


@app.route('/get_data',methods=['GET'])
def get_data():
    phone_number = request.args.get('phone_number')

    phone_number_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/form/div[1]/div[2]/div/div/div[3]/input')
    phone_number_input.clear()
    phone_number_input.send_keys(str(phone_number))

    # Find the button element by its type attribute
    button_element = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/form/div[2]/button")
    button_element.click()

    # Wait for the element to be present on the page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div'))
    )

    try:
        # Wait for the element to be present on the page
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div[1]/div/div[3]/textarea'))
        )

        # Find the textarea element
        textarea_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div[1]/div/div[3]/textarea')
        # Get the text from the textarea
        textarea_text = textarea_element.get_attribute('value')

        return f'{textarea_text}'
    except:
        return '{"status":"failed"}'


if __name__ == '__main__':
    app.run(debug=True)

# Remember to quit the Selenium WebDriver when the Flask app is shut down
@app.teardown_appcontext
def teardown_context(exception=None):
    driver.quit()
