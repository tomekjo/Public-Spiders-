import urllib3, re, lxml.html, csv
import urllib.parse, time

def download(url):
	# getting html as a text
	print('Downloading', url)
	try:
		headers = {'User-agent': 'ti'}
		http = urllib3.PoolManager(num_pools=10, headers=headers)
		r = http.request('GET', url)
		print ('Status of download:', r.status)
		page_html = r.data.decode()
	except urllib3.exceptions.HTTPError as e:
		print('Download error', e.reason)
		page_html = None
	return page_html

def get_data(page_html):
	# from html it is extracted required data to global list
		
	#creation of tree object for lxml
	tree = lxml.html.fromstring(page_html)
		
	#preparation lists with data
	title = tree.cssselect('#causes-index > div > div.ui.three.column.grid.stackable > div > div > a:nth-child(2) > div.content > h3')
	#info = tree.cssselect('#causes-index > div > div.ui.three.column.grid.stackable > div > div > a:nth-child(2) > div.content > p')
	ilink = tree.cssselect('#causes-index > div > div.ui.three.column.grid.stackable > div > div > a:nth-child(2)')
	amount = tree.cssselect('#causes-index > div > div.ui.three.column.grid.stackable > div > div > a:nth-child(2) > div.content > div > div.sp-progressbar > div > div > span')
	percent = tree.cssselect('#causes-index > div > div.ui.three.column.grid.stackable > div > div > a:nth-child(2) > div.content > div > div.sp-progressbar > div > div > small > span')
	missing = tree.cssselect('#causes-index > div > div.ui.three.column.grid.stackable > div > div > a:nth-child(2) > div.content > div > div.still-missing')
		
	#iteration for records of data 
	for d in range(len(title)):
		li = []
		li.append(title[d].text_content())
		li.append(urllib.parse.urljoin(source, ilink[d].attrib['href']))
		li.append(amount[d].attrib['data-value'].replace('.',','))
		li.append(percent[d].attrib['data-value'].replace('.',','))
		try:
			li.append(re.search('[0-9]* [0-9]+', missing[d].text_content()).group())
		except:
			li.append(0)		
		
		#replenishment of the global list with each record
		helplist.append(li)

	#checkin if it is more pages
	link_more = tree.cssselect('#causes-index > div > p > a')
	next_url = urllib.parse.urljoin(source, link_more[0].attrib['href'])
	
	return next_url

def save_in_csv(lista):
	#saving list into csv file
	with open ('inneedlist.csv', 'w') as new_file:
		csv_writer = csv.writer(new_file)

		for line in lista:
			csv_writer.writerow(line)

	return

def crawl_the_page(url):
	time.sleep(1)
	html = download(url)
	next_url = get_data(html)
	
	try:
		if next_url:
			crawl_the_page(next_url)
	except:
		print("Koniec pobierania")
		return

#starting url
source = 'https://www.siepomaga.pl/potrzebujacy'

#initialisation of global list with names of columns
helplist = [['tytuł','link', 'kwota zebrana', 'procent zebrany', 'kwota brakująca']]

crawl_the_page(source)

save_in_csv(helplist)



