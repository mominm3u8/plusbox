import requests
from bs4 import BeautifulSoup
import re


def scrape_links(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    # print(response.text)

    # Find all elements with data-source attribute and filter links
    for element in soup.find_all(attrs={'data-source': True}):
        link = element['data-source']
        if re.match(r'http://plusbox\.tv:8080/[^/]+/embed\.html\?mute=false&autoplay=true&volume=50&token=', link):
            variable = link.split('/')[-2]  # Extract the variable from the original link
            token = get_token(variable)
            new_link = f'http://plusbox.tv:8080/{variable}/index.fmp4.m3u8?token={token}'
            links.append(new_link)

    return links


def get_token(variable):
    # print(variable)
    url = 'http://www.plusbox.tv/token.php'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://www.plusbox.tv',
        'Referer': 'http://www.plusbox.tv/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {'ch_name': variable}
    response = requests.post(url, headers=headers, data=data)
    # print(response.text)  # Check the response for the token
    return response.text  # Assuming the token is in the response text


def save_to_m3u(links):
    with open('channels.m3u', 'w') as f:
        f.write('#EXTM3U\n')  # M3U header
        for link in links:
            channel_name = link.split('/')[-2]  # Extract channel name from link
            f.write(f'#EXTINF:-1,{channel_name}\n')
            f.write(f'{link}\n')


def save_to_m3u_with_channel_names(links):
    with open('channels_with_names.m3u', 'w') as f:
        f.write('#EXTM3U\n')  # M3U header
        for link in links:
            channel_name = link.split('/')[-2]  # Extract channel name from link
            f.write(f'#EXTINF:-1,{channel_name}\n')
            f.write(f'{link}\n')


if __name__ == '__main__':
    url = 'http://www.plusbox.tv/'
    scraped_links = scrape_links(url)
    save_to_m3u(scraped_links)  # Save the final links in M3U format
    # save_to_m3u_with_channel_names(scraped_links)  # Save the final links in M3U format with channel names
    # for link in scraped_links:
    #     print(link)