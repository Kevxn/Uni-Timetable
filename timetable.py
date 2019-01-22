import sys
import json
import requests

s = requests.Session()

headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
	"Cache-Control": "no-cache",
	"Connection": "keep-alive",
	"Content-Length": "421", # doesnt seem to matter
	"Content-Type": "application/x-www-form-urlencoded",
	"Host": "celcat.gcu.ac.uk",
	"Origin": "https://celcat.gcu.ac.uk",
	"Pragma": "no-cache",
	"Referer": "https://celcat.gcu.ac.uk/calendar/Login.aspx",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

form_data = {
	"__VIEWSTATE": "/wEPDwUJMzU2NTg3MDE4D2QWAgIDD2QWAgIRDw8WBB4EVGV4dGUeB1Zpc2libGVoZGRk5cNWEVgGDQZtNYfVOk20Xl6ClWjlDsbX4PP5XSaILkQ=",
	"__VIEWSTATEGENERATOR": "B03196AA",
	"__EVENTVALIDATION": "/wEdAARWb5WOn8g8skyQRpeOOBIvY3plgk0YBAefRz3MyBlTcA6Puailico2fWp193TJgzGinihG6d/Xh3PZm3b5AoMQOSY6sffflldTJvgCRO34bCZ64yAnmLHLUfA/PRsW0fA=",
	"txtUserName": sys.argv[1],
	"txtUserPass": sys.argv[2],
	"btnLogin":    "Log In"   
}

timetable_headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
	"Cache-Control": "no-cache",
	"Connection": "keep-alive",
	"Host": "celcat.gcu.ac.uk",
	"Pragma": "no-cache",
	"Referer": "https://celcat.gcu.ac.uk/calendar/Login.aspx",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

def parse_timetable_data(timetable_data, days_info):
	events = []
	for event in data:
		try:
			_class = event['text'].split('<br>')
			class_name = _class[0]
			class_room = _class[2]
			class_lecturer = _class[3]
			class_time = _class[4]
			class_type = _class[5]

			events.append({
					"week_beginning": event['resource'],
					"day": calc_days(days_info, event['start'][0:10]),
					"class_title": class_name.strip(),
					"class_room": class_room.replace('</b>', '').replace('<b>', '').strip(),
					"class_lecturer": class_lecturer,
					"class_time": class_time,
					"class_type": class_type
				})
		except:
			pass
			# could be holiday? should really handle this
	return json.dumps(events)

def calc_days(days_data, event_start):
	for day in days_data[0]:
		if day['start'] == event_start:
			return day['innerHTML']

r = s.post("https://celcat.gcu.ac.uk/calendar/Login.aspx", headers=headers, data=form_data)

timetable = s.get("https://celcat.gcu.ac.uk/calendar/default.aspx", headers=timetable_headers)
get_json = timetable.text.split('v.events.list')[1].split('v.links.list')[0].replace(' = ', '')
get_days = timetable.text.split('v.timeHeader')[1].split('v.timeline')[0].replace(' = ', '')

days_data = json.loads(get_days.strip()[:-1])
data = json.loads(get_json.strip()[:-1])

timetable = parse_timetable_data(data, days_data)

try:
	with open("events_timetable.json", "w") as f:
		f.write(timetable)
		print("Output written to events_timetable.json")
except:
	print("Couldn't write output to file, dumping output...")
	print(timetable)
