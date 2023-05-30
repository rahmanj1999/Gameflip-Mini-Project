import time
import csv
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from random import randint

#This programs gets the amount of items along with the items available to sell on my profile
base_url = 'https://gameflip.com'

#Method to get the name of the listing along with the price of the listing
def get_info(html):
    soup = bs(html, 'html5lib')

    listings = soup.find_all('div', {'class': 'listing-detail'})
    results = []
    for l in listings:
        name = l.p.text
        price = l.find('span', {'class': 'money'}).text
        price = price[1:]
        
        results.append([name, price])

    try:
        next_page = base_url + soup.find('span', {'class': 'fa fa-chevron-right'}).parent.get('href')
    except:
        next_page = ''

    return results, next_page

#method to concatenate duplicate items
def count_occurence(lst):
    counted_list = []
    for i in lst:
        occ = lst.count(i)
        counted_list.append(i + [occ])

    sorted_list = sorted(set(tuple(row) for row in counted_list))

    return sorted_list

#writes listing along with amount to csv file
def write_to_csv(lst, filename):  # save list of lists to csv
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([
            'Card Name',
            'Price',
            'Quantity'
            ])
        for i in lst:
            writer.writerow(i)


def main():
    while True:
        search_url = "https://gameflip.com/profile/us-east-1:10952500-b0e4-425d-ad0f-91db0a74d2e3/giftcardmaster?limit=36&page=1&status=onsale"
        if not search_url.startswith(base_url):
            print(f'[!] Please enter the URL from "{base_url}"')
            continue
        break

    total_results = []
    page_num = 1
    while True:
        print('[-] Scraping page', page_num)
        r = requests.get(search_url)
        page_results, next_page = get_info(r.text)
        print(page_results)
        total_results += page_results
        if not next_page:
            break
        search_url = next_page

        page_num += 1
        time.sleep(randint(2,6))

    sorted_list = count_occurence(total_results)

    filename = datetime.now().strftime('results_%Y-%m-%d_%H-%M.csv')
    write_to_csv(sorted_list, filename)
    print(f'\n[i] Successfully saved under "{filename}"')


if __name__ == '__main__':
    main()
