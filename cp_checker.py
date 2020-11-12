from bs4 import BeautifulSoup
from string import printable
from datetime import datetime, timedelta
import requests
import json
import time

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def format_string(string, extra=''):
    remove_uc = ''
    for i in string:
        if i in printable: remove_uc += i
    return remove_uc.strip().replace('\n', '').replace('\r', '').replace('\t', '').replace(extra, '')

def format_time(dt):
    return dt.strftime("%H:%M | %d %b 20%y ({})".format(days[dt.weekday()]))

outfile = open('output.txt', 'w+')
def iterate_dict(dict1, ex_str):
    for k1, v1 in dict1.items():
        outfile.write(k1 + ' (' + ex_str + ') ' + '\n')
        for k2, v2 in v1.items():
            if v2 != '': 
                if type(v2) == list: outfile.write(k2 + ': ' + ', '.join(v2) + '\n')
                else: outfile.write(k2 + ': ' + v2 + '\n')
        outfile.write('\n')

print('Running...')

codechef, codeforces, atcoder = {}, {}, {}

# Codechef

URL = "https://www.codechef.com/contests"
r = requests.get(URL) 
soup = BeautifulSoup(r.content, 'html.parser')

ch_tbs = soup.find_all('table', class_='dataTable')[:2]
for ch_tb in ch_tbs:
    ch_rows = ch_tb.find_all('tr')
    for ch_row in ch_rows:
        ch_cols = ch_row.find_all('td')
        ch_col_texts = []
        for ch_col in ch_cols: ch_col_texts.append(format_string(ch_col.text))
        if ch_col_texts != []:
            ch_start_arr = ch_col_texts[2].split()
            ch_start_dt = datetime(
                int(ch_start_arr[2]), 
                months.index(ch_start_arr[1]) + 1, 
                int(ch_start_arr[0]),
                int(ch_start_arr[len(ch_start_arr) - 1].split(':')[0]),
                int(ch_start_arr[len(ch_start_arr) - 1].split(':')[1]),
                int(ch_start_arr[len(ch_start_arr) - 1].split(':')[2])
            ) + timedelta(hours=+3.5)
            ch_end_arr = ch_col_texts[3].split()
            ch_end_dt = datetime(
                int(ch_end_arr[2]), 
                months.index(ch_end_arr[1]) + 1, 
                int(ch_end_arr[0]),
                int(ch_end_arr[len(ch_end_arr) - 1].split(':')[0]),
                int(ch_end_arr[len(ch_end_arr) - 1].split(':')[1]),
                int(ch_end_arr[len(ch_end_arr) - 1].split(':')[2])
            ) + timedelta(hours=+3.5)
            codechef[ch_col_texts[1]] = {
                'code': ch_col_texts[0],
                'author': '',
                'start': format_time(ch_start_dt),
                'end': format_time(ch_end_dt)
            }

# Codeforces

URL = "https://codeforces.com/contests"
r = requests.get(URL) 
soup = BeautifulSoup(r.content, 'html.parser')

cf_tb = soup.find('table')
cf_rows = cf_tb.find_all('tr')
for cf_row in cf_rows:
    cf_cols = cf_row.find_all('td')
    cf_col_texts = []
    try: cf_code = cf_row['data-contestid']
    except KeyError: pass
    for cf_col in cf_cols:
        cf_as = cf_col.find_all('a')
        if cf_as != [] and len(cf_as) > 1:
            cf_a_texts = []
            for cf_a in cf_as: cf_a_texts.append(format_string(cf_a.text))
            cf_col_texts.append(cf_a_texts)
        else: cf_col_texts.append(format_string(cf_col.text))
    cf_col_texts = cf_col_texts[:len(cf_col_texts) - 2]
    if cf_col_texts != []:
        cf_start_date = cf_col_texts[2].split()[0].split('/')
        cf_start_time = cf_col_texts[2].split()[1].split(':')
        cf_start_dt = datetime(
            int(cf_start_date[2]),
            months.index(cf_start_date[0]) + 1,
            int(cf_start_date[1]),
            int(cf_start_time[0]),
            int(cf_start_time[1])
        ) + timedelta(hours=6)
        if cf_col_texts[3].count(':') == 1:
            cf_end_dt = cf_start_dt + timedelta(hours=int(cf_col_texts[3].split(':')[0]), minutes=int(cf_col_texts[3].split(':')[1]))
        elif cf_col_texts[3].count(':') == 2:
            cf_end_dt = cf_start_dt + timedelta(
                days=int(cf_col_texts[3].split(':')[0]), 
                hours=int(cf_col_texts[3].split(':')[1]), 
                minutes=int(cf_col_texts[3].split(':')[2])
            )
        codeforces[cf_col_texts[0]] = {
            'code': cf_code,
            'author': cf_col_texts[1],
            'start': format_time(cf_start_dt),
            'end': format_time(cf_end_dt)
        }


# Atcoder

URL = "https://atcoder.jp/"
r = requests.get(URL) 
soup = BeautifulSoup(r.content, 'html.parser')

at_tb = soup.find_all('table')[1]
at_rows = at_tb.find_all('tr')
for at_row in at_rows:
    at_cols = at_row.find_all('td')
    at_col_texts = []
    for at_col in at_cols: at_col_texts.append(format_string(at_col.text, '+0900'))
    if at_col_texts != []:
        at_start_date = at_col_texts[0].split()[0].split('-')
        at_start_time = at_col_texts[0].split()[1].split(':')
        at_start_dt = datetime(
            int(at_start_date[0]),
            int(at_start_date[1]),
            int(at_start_date[2]),
            int(at_start_time[0]),
            int(at_start_time[1]),
            int(at_start_time[2])
        )
        atcoder[at_col_texts[1]] = {
            'code': '',
            'author': '',
            'start': format_time(at_start_dt),
            'end': format_time(at_start_dt + timedelta(hours=2))
        }

contests = {
    'Codechef': codechef,
    'Codeforces': codeforces,
    'Atcoder': atcoder
}

with open('output.json', 'w+') as handle: json.dump(contests, handle, indent=4)
for key, value in contests.items(): iterate_dict(value, key)

print('Program has finished running. You should see an output.txt and an output.json file.')
time.sleep(1)
