from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import csv
import requests

def pbp_stats():
    URL = "https://api.pbpstats.com/get-totals/nba?Season=2022-23&SeasonType=Regular%2BSeason&Type=Player"

    r = requests.get(url=URL)

    # extracting data in json format
    data = r.json()['multi_row_table_data']
    relevant_stats = {}
    for record in data:
        games_played = record['GamesPlayed']
        mpg = round(record['Minutes']/games_played,1)
        if 'Steals' in record:
            steals = round(record['Steals']/games_played,1)
        else:
            steals = 0
        if 'Blocks' in record:
            if 'BlockedAtRim' in record:
                blocks_rim = round(record['BlockedAtRim'] / games_played, 1)
                blocks_perimeter = round((record['Blocks'] - record['BlockedAtRim']) / games_played, 1)
            else:
                blocks_perimeter = round(record['Blocks']/games_played,1)
        else:
            blocks_perimeter = 0
            blocks_rim = 0
        if 'Charge Fouls Drawn' in record:
            charges = round(record['Charge Fouls Drawn']/games_played,2)
        else:
            charges = 0
        relevant_stats[record['Name']] = [mpg, steals, blocks_perimeter, mpg, charges, blocks_rim]
    return relevant_stats

def traditional_stats():
    url = 'https://www.nba.com/stats/players/traditional'

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))

    driver.get(url)

    selects = driver.find_elements(By.CLASS_NAME, "DropDown_select__4pIg9 ")
    for select in selects:
        options = Select(select).options

    for option in options:
        if option.text == 'All':
            option.click() # select() in earlier versions of webdriver
            break

    # Find the table element
    table = driver.find_element(By.CLASS_NAME, 'Crom_table__p1iZz')

    # Find all rows in the table
    rows = table.find_elements(By.TAG_NAME, 'tr')
    traditional_stats = {}
    # Loop through each row and extract the data from each cell
    for row in rows:
        i=0
        # Find all cells in the row
        cells = row.find_elements(By.TAG_NAME, 'td')
        player=''
        player_stats = []
        for cell in cells:
            if i==1:
                player = cell.text
            elif i==7:
                player_stats.append(cell.text)
            elif i==23:
                player_stats.append(cell.text)
            i+=1
        traditional_stats[player] = player_stats
    return traditional_stats

def team_defenses():
    url = 'https://www.nba.com/stats/teams/defense'

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))

    driver.get(url)

    # Find the table element
    table = driver.find_element(By.CLASS_NAME, 'Crom_table__p1iZz')

    # Find all rows in the table
    rows = table.find_elements(By.TAG_NAME, 'tr')
    team_defenses = []
    # Loop through each row and extract the data from each cell
    for row in rows:
        i=0
        # Find all cells in the row
        cells = row.find_elements(By.TAG_NAME, 'td')
        team=''
        def_rtg = 0
        opp_pts_paint = 0
        for cell in cells:
            if i==1:
                team = cell.text
            elif i==6:
                def_rtg = float(cell.text)
            elif i==14:
                opp_pts_paint = float(cell.text)
            i+=1
        if team:
            team_defenses.append([get_team_abbrivation(team), round(def_rtg-opp_pts_paint,1), opp_pts_paint])
    header = ['Team', 'PDEF', 'RDEF']
    with open('team_defenses.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(team_defenses)

def get_team_abbrivation(fullname):
    if fullname == "Milwaukee Bucks":
        return "MIL"
    elif fullname == "Boston Celtics":
        return "BOS"
    elif fullname == "Denver Nuggets":
        return "DEN"
    elif fullname == "Philadelphia 76ers":
        return "PHI"
    elif fullname == "Cleveland Cavaliers":
        return "CLE"
    elif fullname == "Memphis Grizzlies":
        return "MEM"
    elif fullname == "New York Knicks":
        return "NYK"
    elif fullname == "Sacramento Kings":
        return "SAC"
    elif fullname == "Brooklyn Nets":
        return "BKN"
    elif fullname == "Phoenix Suns":
        return "PHX"
    elif fullname == "Miami Heat":
        return "MIA"
    elif fullname == "LA Clippers":
        return "LAC"
    elif fullname == "Atlanta Hawks":
        return "ATL"
    elif fullname == "Dallas Mavericks":
        return "DAL"
    elif fullname == "Golden State Warriors":
        return "GSW"
    elif fullname == "Minnesota Timberwolves":
        return "MIN"
    elif fullname == "Los Angeles Lakers":
        return "LAL"
    elif fullname == "New Orleans Pelicans":
        return "NOP"
    elif fullname == "Toronto Raptors":
        return "TOR"
    elif fullname == "Utah Jazz":
        return "UTA"
    elif fullname == "Oklahoma City Thunder":
        return "OKC"
    elif fullname == "Portland Trail Blazers":
        return "POR"
    elif fullname == "Washington Wizards":
        return "WAS"
    elif fullname == "Chicago Bulls":
        return "CHI"
    elif fullname == "Indiana Pacers":
        return "IND"
    elif fullname == "Orlando Magic":
        return "ORL"
    elif fullname == "Charlotte Hornets":
        return "CHA"
    elif fullname == "San Antonio Spurs":
        return "SAS"
    elif fullname == "Detroit Pistons":
        return "DET"
    elif fullname == "Houston Rockets":
        return "HOU"

def defense_dash_gt15(pbp_stats):
    # Defense dash for greater than 15
    url = 'https://www.nba.com/stats/players/defense-dash-gt15'

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))

    driver.get(url)

    selects = driver.find_elements(By.CLASS_NAME, "DropDown_select__4pIg9 ")
    for select in selects:
        options = Select(select).options

    for option in options:
        if option.text == 'All':
            option.click() # select() in earlier versions of webdriver
            break

    # Find the table element
    table = driver.find_element(By.CLASS_NAME, 'Crom_table__p1iZz')

    # Find all rows in the table
    rows = table.find_elements(By.TAG_NAME, 'tr')
    defense_dash_gt15 = []
    # Loop through each row and extract the data from each cell
    for row in rows:
        player_dd_gt15 = []
        # Find all cells in the row
        cells = row.find_elements(By.TAG_NAME, 'td')
        for cell in cells:
            player_dd_gt15.append(cell.text)
        # Add pbp stats to defense_dash if not empty
        if player_dd_gt15:
            if player_dd_gt15[0] in pbp_stats:
                defense_dash_gt15.append(player_dd_gt15 + pbp_stats[player_dd_gt15[0]][:3])
            else:
                defense_dash_gt15.append(player_dd_gt15 + ['NaN', 'NaN', 'NaN'])


    header = ['Player', 'Team', 'Age', 'Position', 'GP', 'Games', 'FREQ%', 'DFGM', 'DFGA', 'DFG%', 'FG%', 'DIFF%', "MP", "STL", "BLKP"]
    with open('defense_dash_gt15.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(defense_dash_gt15)

def defense_dash_lt10(pbp_stats):
    # Less than 10 foot
    url = 'https://www.nba.com/stats/players/defense-dash-lt10'

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))

    driver.get(url)

    selects = driver.find_elements(By.CLASS_NAME, "DropDown_select__4pIg9 ")
    for select in selects:
        options = Select(select).options

    for option in options:
        if option.text == 'All':
            option.click() # select() in earlier versions of webdriver
            break

    # Find the table element
    table = driver.find_element(By.CLASS_NAME, 'Crom_table__p1iZz')

    # Find all rows in the table
    rows = table.find_elements(By.TAG_NAME, 'tr')
    defense_dash_lt10 = []

    # Loop through each row and extract the data from each cell
    for row in rows:
        player_dd_lt10 = []
        # Find all cells in the row
        cells = row.find_elements(By.TAG_NAME, 'td')
        for cell in cells:
                player_dd_lt10.append(cell.text)
        # Add pbp stats to defense dash if not empty
        if player_dd_lt10:
            if player_dd_lt10[0] in pbp_stats:
                defense_dash_lt10.append(player_dd_lt10 + pbp_stats[player_dd_lt10[0]][-3:])
            else:
                defense_dash_lt10.append(player_dd_lt10 + ['NaN', 'NaN', 'NaN'])


    header = ['Player', 'Team', 'Age', 'Position', 'GP', 'Games', 'FREQ%', 'DFGM', 'DFGA', 'DFG%', 'FG%', 'DIFF%', "MP", "Charges", "BLKR"]
    with open('defense_dash_lt10.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(defense_dash_lt10)

#pbp_stats = pbp_stats()
#traditional_stats = traditional_stats()
#defense_dash_gt15(pbp_stats)
#defense_dash_lt10(pbp_stats)
team_defenses()