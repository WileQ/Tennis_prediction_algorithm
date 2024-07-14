from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def rankAndId(player, proxy = None):
    """Returns rank and ID of the player."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    if proxy != None:
        options.add_argument(f"--proxy-server={proxy}")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.ultimatetennisstatistics.com/")

    wait = WebDriverWait(driver, 20)
    manage_options_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='fc-button-label']")))
    manage_options_button.click()

    search_bar = driver.find_element(By.ID, "player")

    search_bar.send_keys(player)
    time.sleep(1)
    search_bar.send_keys(Keys.ARROW_DOWN)
    search_bar.send_keys(Keys.ENTER)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "lxml")

    ranking = ""
    for tekst in soup.findAll("tr"):
        for i in range(len(tekst.text.splitlines())):
            if tekst.text.splitlines()[i] == "Current Rank":
                ranking = tekst.text.splitlines()[i + 1]

    rank = int(ranking.split()[0])

    name = ""
    for tekst in soup.find("h3"):
        for i in range(len(tekst.text.splitlines())):
            if tekst.text.splitlines()[i] != "":
                name = tekst.text.splitlines()[i]

    name = name.strip()

    stat_link = driver.current_url[:-7] + "statistics"

    return [rank, stat_link, name]

def playerData(opponentRank, statlink, proxy = None):
    """Returns the data collected from Ultimate Tennis Statistics website about the player."""

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    if proxy != None:
        options.add_argument(f"--proxy-server={proxy}")
    driver = webdriver.Chrome(options=options)

    url = statlink
    driver.get(url)

    year = str(date.today().year - 1)

    rank = ""
    if opponentRank <= 20:
        rank = "Vs Top 20"
    elif opponentRank <= 50:
        rank = "Vs Top 50"
    elif opponentRank <= 100:
        rank = "Vs Top 100"
    else:
        rank = "Vs all"

    try:
        dropbox = driver.find_elements(by=By.TAG_NAME, value="Option")
        for i in range(len(dropbox)):
            if str(dropbox[i].text) == rank:
                dropbox[i].click()
            if str(dropbox[i].text) == year:
                dropbox[i].click()
    except:
        pass

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'lxml')

    ace = ""
    double_fault = ""
    first_serve = ""
    first_serve_won = ""
    second_serve_won = ""
    ace_against = ""
    first_serve_return_won = ""
    second_serve_return_won = ""

    for tekst in soup.findAll("tbody"):
        for i in range(len(tekst.text.splitlines())):
            if tekst.text.splitlines()[i] == "Ace %":
                ace = float(tekst.text.splitlines()[i + 1][:-1])
            if tekst.text.splitlines()[i] == "Double Fault %":
                double_fault = float(tekst.text.splitlines()[i + 1][:-1])
            if tekst.text.splitlines()[i] == "1st Serve %":
                first_serve = float(tekst.text.splitlines()[i + 1][:-1])
            if tekst.text.splitlines()[i] == "1st Serve Won %":
                first_serve_won = float(tekst.text.splitlines()[i + 1][:-1])
            if tekst.text.splitlines()[i] == "2nd Serve Won %":
                second_serve_won = float(tekst.text.splitlines()[i + 1][:-1])
            if tekst.text.splitlines()[i] == "Ace Against %":
                ace_against = float(tekst.text.splitlines()[i + 1][:-1])
            if tekst.text.splitlines()[i] == "1st Srv. Return Won %":
                first_serve_return_won = float(tekst.text.splitlines()[i + 1][:-1])
            if tekst.text.splitlines()[i] == "2nd Srv. Return Won %":
                second_serve_return_won = float(tekst.text.splitlines()[i + 1][:-1])

    return [ace, double_fault, first_serve, first_serve_won, second_serve_won, ace_against, first_serve_return_won, second_serve_return_won]


def getInputs():
    """Returns data required for the simulation to work."""
    n = int(input("How many game do you want to simulate: "))
    sets_in_a_match = int(input("Is this a best of 3 or best of 5: "))
    playerA = input("Write the full name of the tennis player who is going to serve first: ")
    playerB = input("Write the full name of the tennis player who is going to serve second: ")
    if_proxy = input("Do you want to use a proxy? ")
    if if_proxy.lower() == "yes":
        proxy = input("Input your proxy - (ip):(port) ")
    else:
        proxy = None

    rankingAndIdA = rankAndId(playerA, proxy)
    rankingAndIdB = rankAndId(playerB, proxy)

    rankA = rankingAndIdA[0]
    rankB = rankingAndIdB[0]
    idA = rankingAndIdA[1]
    idB = rankingAndIdB[1]
    playerA = rankingAndIdA[2]
    playerB = rankingAndIdB[2]

    dataPlayerA = playerData(rankB, idA, proxy)
    dataPlayerB = playerData(rankA, idB, proxy)

    firstserveA = dataPlayerA[2]/100
    winsfirstA = (dataPlayerA[3] + dataPlayerB[6])/200
    winssecondA = (dataPlayerA[4] + dataPlayerB[7])/200
    aceA = (dataPlayerA[0] + dataPlayerB[5])/200
    dfA = dataPlayerA[1]/100

    firstserveB = dataPlayerB[2]/100
    winsfirstB = (dataPlayerB[3] + dataPlayerA[6]) / 200
    winssecondB = (dataPlayerB[4] + dataPlayerA[7]) / 200
    aceB = (dataPlayerB[0] + dataPlayerA[5]) / 200
    dfB = dataPlayerB[1]/100

    if sets_in_a_match == 3:
        sets_in_a_match = 2
    if sets_in_a_match == 5:
        sets_in_a_match = 3

    return firstserveA, winsfirstA, winssecondA, aceA, dfA, firstserveB, winsfirstB, winssecondB, aceB, dfB, n, playerA, playerB, sets_in_a_match