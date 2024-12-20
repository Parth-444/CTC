from bs4 import BeautifulSoup

url = "https://databox.com/ppc-industry-benchmarks"
response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
else:
    print(f"Failed to fetch webpage: {response.status_code}")

soup = BeautifulSoup(html_content, 'html.parser')

tables = soup.find_all('table')

def extract_cpc_data(table):
    rows = table.find_all('tr')
    cpc_data = {}
    for row in rows[1:]:
        cols = row.find_all('td')
        industry = cols[0].text.strip()
        cpc = cols[1].text.strip()
        if cpc=='MISSING':
            cpc='0'
        cpc = cpc.replace('$', '').replace('<strong>', '').replace('</strong>', '').strip()
        cpc_data[industry] = float(cpc) if cpc else 0.0
    return cpc_data

def extract_clicks_data(table):
    rows = table.find_all('tr')
    clicks_data = {}
    for row in rows[1:]:
        cols = row.find_all('td')
        industry = cols[0].text.strip()
        clicks = cols[1].text.strip()
        if clicks=='MISSING':
            clicks='0'
        clicks = clicks.replace('<strong>', '').replace('</strong>', '').strip()
        if 'K' in clicks:
            clicks = float(clicks.replace('K', '').strip()) * 1000
        else:
            clicks = float(clicks)
        clicks_data[industry] = int(clicks)
    return clicks_data


google_clicks=extract_clicks_data(tables[3])
google_cpc=extract_cpc_data(tables[9])
facebook_clicks=extract_clicks_data(tables[4])
facebook_cpc=extract_cpc_data(tables[10])
linkedin_clicks=extract_clicks_data(tables[5])
linkedin_cpc=extract_cpc_data(tables[11])


ctc_google={industry: google_cpc[industry] * google_clicks[industry] for industry in google_cpc if industry in google_clicks}
ctc_facebook={industry: facebook_cpc[industry] * facebook_clicks[industry] for industry in facebook_cpc if industry in facebook_clicks}
ctc_linkedin={industry: linkedin_cpc[industry] * linkedin_clicks[industry] for industry in linkedin_cpc if industry in linkedin_clicks}

print("Google Ads CTC Calculation:")
for (key, values) in ctc_google.items():
    print(f'{key}: CTC = {values}')
print()
print("Facebook Ads CTC Calculation:")
for (key, values) in ctc_facebook.items():
    print(f'{key}: CTC = {values}')
print()
print("Linkedin Ads CTC Calculation:")
for (key, values) in ctc_linkedin.items():
    print(f'{key}: CTC = {values}')