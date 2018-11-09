import random
import os
import glob
from os import environ

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

SCREEN_SHOT_PATH = environ.get('SCREEN_SHOT_PATH')
EXPERIMENT_URL = environ.get('EXPERIMENT_URL')
PHASE_ONE_ROUNDS = 4
NUMBER_OF_TASKS = 6


def play_instructions(browser, phase):
    browser.save_screenshot('{}/phase_{}_instructions.png'.format(SCREEN_SHOT_PATH, phase))
    browser.find_element(By.XPATH, '//button').click()


def play_outcome(browser, phase):
    browser.save_screenshot('{}/phase_{}_outcome.png'.format(SCREEN_SHOT_PATH, phase))
    browser.find_element(By.XPATH, '//button').click()


def play_phase_one_bid(browser, round_number):
    if round_number == 1:
        browser.save_screenshot('{}/phase_one_bid_screen.png'.format(SCREEN_SHOT_PATH))

    min_value = int(browser.find_element_by_id("id_bid").get_attribute('min'))
    max_value = int(browser.find_element_by_id("id_bid").get_attribute('max'))
    input_field = browser.find_element(By.XPATH, "//input[@id='id_bid']")
    input_field.clear()
    random_bid = random.randint(min_value, max_value)
    print("Phase 1: Entered Bid {}".format(random_bid))
    input_field.send_keys(str(random_bid))
    browser.find_element(By.XPATH, '//button').click()


def enter_password(browser):
    browser.save_screenshot('{}/phase_two_password_screen.png'.format(SCREEN_SHOT_PATH))

    input_field = browser.find_element(By.XPATH, "//input[@id='pass_code']")
    input_field.clear()
    print("Phase 2: Entered Password")
    input_field.send_keys("2600")
    browser.find_element(By.XPATH, '//button').click()


def choose_color_and_bet(browser, task_number):
    browser.save_screenshot('{}/phase_choose_color_bet_task_{}.png'.format(task_number, SCREEN_SHOT_PATH))

    browser.find_element(By.XPATH, "//input[@id='clicked']").value = '1'
    if random.randint(0, 1) == 0:
        print('Stage 4: Betting high on Red')
        browser.find_element(By.XPATH, "//button[@id='red-bet-button']").click()
    else:
        print('Stage 4: Betting high on Blue')
        browser.find_element(By.XPATH, "//button[@id='blue-bet-button']").click()

    min_value = int(browser.find_element_by_id("cutoff").get_attribute('min'))
    max_value = int(browser.find_element_by_id("cutoff").get_attribute('max'))
    browser.execute_script("""$('input[type="range"]').val({}).change();""".format(random.randint(min_value, max_value)))
    browser.find_element(By.XPATH, "//button[@id='next-button']").click()


def roll_die(browser):
    browser.save_screenshot('{}/phase_four_roll_die_screen.png'.format(SCREEN_SHOT_PATH))
    browser.find_element(By.XPATH, "//button[@id='die-button']").click()
    die_side = int(browser.find_element_by_id("side").get_attribute('value'))
    print("Stage 4: Rolled Die Side {}".format(die_side))

    browser.find_element(By.XPATH, "//button[@id='next-button']").click()


def delete_old_screen_shots():
    files = glob.glob(SCREEN_SHOT_PATH + '/*')
    for f in files:
        os.remove(f)


# Run with python -m browser_tests.browser_test
if __name__ == "__main__":
    delete_old_screen_shots()

    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument('--window-size=1200,900')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(30)

    driver.get(EXPERIMENT_URL)
    player_links = driver.find_elements_by_partial_link_text("InitializeParticipant")
    print('there are {} players'.format(len(player_links)))

    for player in range(1, len(player_links) + 1):
        driver.switch_to.window(driver.window_handles[0])
        # create a new tab
        player_links[player-1].send_keys(Keys.COMMAND + Keys.ENTER)

    # Phase 1
    for round_id in range(1, PHASE_ONE_ROUNDS + 1):
        for player in range(1, len(player_links) + 1):
            # switch to new tab
            driver.switch_to.window(driver.window_handles[player])
            if round_id == 1:
                play_instructions(driver, round_id)
            play_phase_one_bid(driver, round_id)

        for player in range(1, len(player_links) + 1):
            driver.switch_to.window(driver.window_handles[player])
            play_outcome(driver, round_id)

    # Phase 2
    for player in range(1, len(player_links) + 1):
        driver.switch_to.window(driver.window_handles[player])
        enter_password(driver)
        roll_die(driver)
        for task_number in range(NUMBER_OF_TASKS):
            choose_color_and_bet(driver, task_number)
