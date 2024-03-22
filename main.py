import requests
from bs4 import BeautifulSoup
from googlesearch import search

markdown = '# Best League of Legends players of all time:\n'

r = requests.get('https://www.redbull.com/int-en/best-league-of-legends-players-of-all-time')
if not r.ok:
    print(r)
    raise Exception('Could not get: https://www.esports.net/news/best-lec-players/')

soup = BeautifulSoup(r.text, 'html.parser')
players = soup.find_all('h2')

for player in players:
    image = player.find_next('a', class_='inline-image__link').get('href')
    player = player.text

    markdown += '### {}\n'.format(player)
    markdown += '![{}]({})\n'.format(player, image)

    googleResults = search('{} lol fandom wiki'.format(player))
    googleResult = next(googleResults)
    print(googleResult)
    r = requests.get(googleResult)
    if not r.ok:
        print(r)
        raise Exception('Could not get: {}'.format(googleResult))

    googleResultSoup = BeautifulSoup(r.text, 'html.parser')
    contentsDiv = googleResultSoup.find(id = 'tocdiv')
    overview = contentsDiv.find_next('p')
    infobox = googleResultSoup.find(id = 'infoboxPlayer')
    playerImage = infobox.find_next('img').get('src')
    playerImage = playerImage[:playerImage.find('.png') + 4]

    for span in overview.find_all('span'):
        span.decompose()

    markdown += '[More about {}](/{}.html)\n'.format(player, player)

    subpageMarkdown = '# More about {}:\n\n'.format(player)
    subpageMarkdown += '![{}]({})\n'.format(player, playerImage)
    subpageMarkdown += overview.text

    with open('{}.md'.format(player), 'w') as file:
        file.write(subpageMarkdown)

with open('index.md', 'w') as file:
    file.write(markdown)
