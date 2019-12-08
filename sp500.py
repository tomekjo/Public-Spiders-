import requests, time
import lxml.html as lh


url_sp500 = r"https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
headers = {'User-Agent': user_agent}


# downloading page with s&p500 companies
def download_site(url):
    response = requests.get(url, headers=headers)
    tree = lh.fromstring(response.text)
    return tree


# creating list with s&p500 symbols
def make_company_list(tree):
    symbols_list = [i.text_content() for i in tree.xpath('//*[@id="constituents"]/tbody/tr/td[1]/a')]
    return symbols_list


# downloading csv with history
def download_csv(company_list):
    with open("sp500.csv", "wt") as out:
        out.write('Data,Otwarcie,Najwyzszy,Najnizszy,Zamkniecie,Wolumen,Symbol\n')
        for i in range(len(company_list)-1):
            # https://stooq.pl/q/d/l/?s=mmm.us&d1=20120102&d2=20191122&i=d
            link_to_csv = 'https://stooq.pl/q/d/l/?s=' + company_list[i] + '.US&d1=20120102&d2=20191122&i=d'
            print(link_to_csv)
            response = requests.get(link_to_csv, headers=headers)

            for row in response.text.splitlines():
                print(row)
                if row.startswith('Data'):
                    pass
                else:
                    row_out = row.rstrip('\n') + ',' + company_list[i] + '\n'
                    out.write(row_out)
                    print(row_out)

            time.sleep(1)


symbols = make_company_list(download_site(url_sp500))
download_csv(symbols)



