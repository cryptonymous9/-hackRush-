# Importing Libraries Required
import json, requests
from pprint import pprint
# Importing Models Defined
from fbchatbot.models import reminder, patient

acc = "EAAQaSFXm09ABAA6Hoh7HxblNQThDwPvMPfKTBGTneVv85iYpRcZCMuZCFsFRsvcxy9sK6pkCcmrInQjcgWQuYdoWWurFcVGfArJi3grBUKYtc36MSs6Itae6TEv8W1jrOvcZApqG5dXbi3RZBwFbS9ZCCtqqtrg61H2mu6YllCL2FbJ74OFl6"

def master_post_fb(fb_id,text):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+acc	
	reply_msg = json.dumps({"recipient":{"id":fb_id}, "message":{"text":text}})
	requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)

def greet_post_fb(fb_id,text):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+acc
	reply_msg = json.dumps({
		"recipient":{"id":fb_id}, 
		"message":{
			"text":text
    	}
    })
	requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)

def post_weather_fb(final_report,fb_id):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+acc	
	reply_msg = json.dumps({
		"recipient":{"id":fb_id},
		"message":{
			"text":final_report,
			}
		}
	)
	requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)


def prescribe_post_fb(number,fb_id):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+acc
	reply_msg = json.dumps({
		"recipient":{"id":fb_id},
		"message":{
			"attachment": {
				"type": "template",
				"payload":{
					"template_type": "button",
					"text": "Sure, fill out this form...",
					"buttons":[
						{
							"type":"web_url",
							"url":"https://cb503686.ngrok.io/fbchatbot/prescription?"+fb_id,
							"title":"Prescription",
							"webview_height_ratio":"tall"
						}
					]
				}
			}
		}
	})
	pprint(reply_msg)
	a=requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)
	# print(a.text)

def buy_post_fb(fb_id):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+acc
	reply_msg = json.dumps({
		"recipient":{"id":fb_id},
		"message":{
			"attachment": {
				"type": "template",
				"payload":{
					"template_type": "button",
					"text": "Sure, fill out this form...",
					"buttons":[
						{
							"type":"web_url",
							"url":"https://www.google.com/search?hl=en&output=search&tbm=shop&psb=1&x=0&y=0&q=iphone+8"+fb_id,
							"title":"Prescribe",
							"webview_height_ratio":"tall"
						}
					]
				}
			}
		}
	})
	pprint(reply_msg)
	a=requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)
	# https://www.google.com/search?hl=en&output=search&tbm=shop&psb=1&x=0&y=0&q=iphone+8

def askLocation(fb_id):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+acc	
	reply_msg = json.dumps({
		"recipient":{"id":fb_id}, 
		"message":{
			"text":'Please Share Your Location',
			"quick_replies":[
				{
       			 "content_type":"location",
      			}
    		]
    	}
    })
	requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)


def getWeather(lat,lon,fb_id):
	appid='b1b15e88fa797225412429c1c50c122a1'
	key="772973e281f73ebc401d23c974de0f09"
	url="https://api.darksky.net/forecast/"+str(key)+"/"+ str(lat) + "," + str(lon)
	#pprint(requests.get(url).json())
	result=requests.get(url).json()
	# pprint(result)
	temp_max=int(((result['daily']['data'][0]['temperatureMax'])-32)*0.5555555555555556)
	temp_min=int(((result['daily']['data'][0]['temperatureMin'])-32)*0.5555555555555556)
	#sunrise=datetime.datetime.fromtimestamp(int(result['daily']['data'][0]['sunriseTime'])).strftime('%H:%M:%S')
	#sunset=datetime.datetime.fromtimestamp(int(result['daily']['data'][0]['sunsetTime'])).strftime('%H:%M:%S')
	#timeZone=(result['timezone'])
	summary=result['hourly']['summary']
	final_report="Max temp : " + str(temp_max) + " °C \n" + "Min temp : " + str(temp_min) + " ° C \n" + "Summary : " + str(summary)
	post_weather_fb(final_report,fb_id)

def cleaning_text(text):
	fresh_text=[]
	for i in range(2,len(text)-1):
		fresh_text.append(text[i])
	fresh_text = "".join(fresh_text)
	return fresh_text

def reminder_fun(fb_id, event, date):
	date, time = make_datetime(date)
	try:
		d = patient.objects.get(contact = fb_id)
	except:		
		patient.objects.create(name = 'name', contact = fb_id)
		d = patient.objects.get(contact = fb_id)									
	reminder.objects.create(event = event, date = date, time = time, user = d)
	text = "Sure ;) , I will remind you about " + event + ', ' + date + '\n :)' 
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+acc	
	reply_msg = json.dumps({"recipient":{"id":fb_id}, "message":{"text":text}})
	return requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)

def make_datetime(datetime):
	date = datetime[:datetime.find('T')]
	time = datetime[datetime.find('T') + 1:datetime.find('.') - 3]
	return date, time