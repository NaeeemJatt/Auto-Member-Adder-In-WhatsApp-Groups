from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

class WhatsAppTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.numberInput = QLineEdit(self)
        self.numberInput.setPlaceholderText('Enter number or list of numbers...')
        layout.addWidget(self.numberInput)

        self.groupFileLabel = QLabel('No file selected', self)
        layout.addWidget(self.groupFileLabel)

        self.fileButton = QPushButton('Select Groups File', self)
        self.fileButton.clicked.connect(self.openFileDialog)
        layout.addWidget(self.fileButton)

        self.startButton = QPushButton('Start Adding Members', self)
        self.startButton.clicked.connect(self.startAddingMembers)
        layout.addWidget(self.startButton)

        self.setLayout(layout)
        self.setWindowTitle('WhatsApp Group Member Adder')
        self.show()

    def openFileDialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt)')
        if file_name:
            self.groupFileLabel.setText(file_name)

    def startAddingMembers(self):
        number = self.numberInput.text()
        group_file = self.groupFileLabel.text()
        if not number or not group_file:
            print("Please provide both the number and group file.")
            return

        try:
            automate_whatsapp(group_file, number)
        except WebDriverException as e:
            print(f"An error occurred while opening Chrome: {e}")

def automate_whatsapp(group_file, number):
    # Try initializing the Chrome WebDriver
    try:
        driver = webdriver.Chrome(executable_path='path/to/chromedriver')  # Update path if necessary
    except WebDriverException as e:
        print(f"Failed to start Chrome WebDriver: {e}")
        return

    # Try opening WhatsApp Web
    try:
        driver.get('https://web.whatsapp.com')
    except WebDriverException as e:
        print(f"Failed to open WhatsApp Web: {e}")
        driver.quit()
        return

    # Wait for the user to scan the QR code
    input("Press Enter after scanning QR code")

    # Read group names from file
    try:
        with open(group_file, 'r') as f:
            groups = f.readlines()
    except Exception as e:
        print(f"Failed to read the group file: {e}")
        driver.quit()
        return

    for group in groups:
        group = group.strip()
        try:
            # Search for the group
            search_box = driver.find_element_by_xpath('//div[@contenteditable="true"]')
            search_box.click()
            search_box.send_keys(group)
            search_box.send_keys(Keys.ENTER)

            time.sleep(2)  # Wait for the group to open

            # Open group info
            driver.find_element_by_xpath('//span[@data-icon="menu"]').click()
            driver.find_element_by_xpath('//div[contains(text(), "Group info")]').click()

            time.sleep(2)  # Wait for group info to open

            # Add participant
            driver.find_element_by_xpath('//span[contains(text(), "Add participant")]').click()
            driver.find_element_by_xpath('//div[@contenteditable="true"]').send_keys(number)
            time.sleep(2)  # Wait for the number to be entered
            driver.find_element_by_xpath('//span[contains(text(), "Add")]').click()

            # Go back to the main WhatsApp window
            driver.find_element_by_xpath('//button[@data-icon="back"]').click()
        except WebDriverException as e:
            print(f"Failed to process group '{group}': {e}")

    driver.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WhatsAppTool()
    sys.exit(app.exec_())
