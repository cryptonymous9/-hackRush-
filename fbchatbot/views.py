#Importing Libraries Required
import json,requests,datetime
from pprint import pprint
from wit import Wit
from pytz import timezone

#Importing Models Defined
from fbchatbot.models import patient, reminder

#Django Shortcuts 
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

#Importing Functions made.
from fbchatbot.chats.functions import(
	master_post_fb,
	greet_post_fb,
	post_weather_fb,
	askLocation,
	getWeather,
	cleaning_text,
	reminder_fun,
	prescribe_post_fb,
	buy_post_fb
)

#Function to check reminders for a particular event
def remind():
    reminders = reminder.objects.all()
    current_reminders=[]
    now = datetime.datetime.now(timezone('Asia/Calcutta'))
    now_strf=now.strftime('%Y %m %d %H %M %S')
    year,month,day,hour,minute,sec=[int(j) for j in now_strf.split()]
    l1=[year,month,day,hour,minute]
    for remindera in reminders:
        date = [int(s) for s in remindera.date.split('-')]
        time = [int(s) for s in remindera.time.split(':')]
        l = date + time
        if l1==l :
            current_reminders.append(remindera)
    if current_reminders != []:
        return(current_reminders)
    else:
        return None

#Function Calling Reminders		
@csrf_exempt
def call_reminder(request):
    h=remind()
    if h != None:
        for i in h:
            master_post_fb(i.user.contact, ':-D Reminder!!! ' + i.user.name + '!\n' + i.event + '\n' + i.time)
            reminder.objects.filter(id=i.id).delete()
    return HttpResponse('ok')

#Prescription form
@csrf_exempt
def index(request):
	return render(request, 'prescription.html')

#Function to handle prescription forms
@csrf_exempt
def prescribe(request):
	fb_id = request.POST.get('fb_id')
	fb_id = ''
	name = request.POST.get('name')
	try:
		d = patient.objects.get(contact = fb_id)
	except:		
		patient.objects.create(name = name, contact = fb_id)
		d = patient.objects.get(contact = fb_id)
	i = 0
	text = 'Your Reminders for medicines prescribed by the doctor are set succesfully :) \n'
	while True:
		tablet_name = 'tablet' + str(i)
		dosage = 'dosage' + str(i)
		quantity = 'quantity' + str(i)
		tablet_name = request.POST.get(tablet_name)
		dosage = request.POST.get(dosage)
		quantity = request.POST.get(quantity)
		if tablet_name == None or dosage == None or quantity == None:
			break
		reminders = make_reminders(d, tablet_name, dosage, quantity)
		text += tablet_name + ' - ' + dosage + ' - ' + quantity + '\n'
		i += 1
	master_post_fb(fb_id, text)
	return HttpResponse('OK')

#
def make_reminders(user, tablet_name, dosage, quantity):
	now = datetime.datetime.now(timezone('Asia/Calcutta'))
	if now.hour <9:
		phase = 0
	elif now.hour<15:
		phase = 1
	else:
		phase = 2
	dosage = dosage.split('-')
	quantity = int(quantity)
	while quantity:
		if phase == 0:
			if dosage[0] == '1':
				reminder.objects.create(user = user, event = tablet_name, date = str(now.date()), time = '09:00')
		elif phase == 1:
			if dosage[1] == '1':
				reminder.objects.create(user = user, event = tablet_name, date = str(now.date()), time = '14:00')
		else:
			if dosage[2] == '1':
				reminder.objects.create(user = user, event = tablet_name, date = str(now.date()), time = '19:00')
		
		phase = (phase + 1)%3
		if phase == 0:
			now = now + datetime.timedelta(hours = 14)
		else:
			now  = now + datetime.timedelta(hours = 5)
		quantity -= 1
		# print('Reminder Succesfully stored!')



wit_access_token = "YWDWPIAONSJYPVRPTLBYNWRPQLJCUROF"

@csrf_exempt
def fbchat(request):
	if request.method == 'GET':
		if request.GET['hub.verify_token'] == '9466123283066123':
			return HttpResponse(request.GET['hub.challenge'])
		else:
			return HttpResponse("Error,invalid token")
	else:
		user_msg=json.loads(request.body.decode('utf-8'))
		pprint(user_msg)
		for entry in user_msg['entry']:
			for message in entry['messaging']:
				fb_id= message['sender']['id']
				if message.get('message'):
					if 'text' in message['message']:
						#handling emojis parts
						if type(message['message']['text'])== bytes:
							message['message']['text']=str(message['message']['text'],"utf-8",errors="ignore")
						else:
							message['message']['text']=str(message['message']['text'])
						# print(fb_id)
						text=message['message']['text']
						# print(text)
						# client.run_actions(session_id=fb_id,message=text)
						msg = client.message(text)
						pprint(msg)
						send(fb_id,msg)
					else:
						#this part will handle the attachement parts for example like button,images etc
						if 'coordinates' in message['message']['attachments'][0]['payload']:
							location=message['message']['attachments'][0]['payload']['coordinates']
							getWeather(location['lat'],location['long'],fb_id)
							
						else:
							text="You liked me"	
							master_post_fb(fb_id,text)
							break # so that api call just happens once and then it exits.

	return HttpResponse()

def send_railway(fb_id, response):
	user_details_url = "https://graph.facebook.com/v2.6/%s"%fb_id
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'EAAQaSFXm09ABAA6Hoh7HxblNQThDwPvMPfKTBGTneVv85iYpRcZCMuZCFsFRsvcxy9sK6pkCcmrInQjcgWQuYdoWWurFcVGfArJi3grBUKYtc36MSs6Itae6TEv8W1jrOvcZApqG5dXbi3RZBwFbS9ZCCtqqtrg61H2mu6YllCL2FbJ74OFl6'}
	user_details = requests.get(user_details_url, user_details_params).json()
	

def send(fb_id,response):
	# fb_id=response['session_id']
	#pprint(request)
	user_details_url = "https://graph.facebook.com/v2.6/%s"%fb_id
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'EAAQaSFXm09ABAA6Hoh7HxblNQThDwPvMPfKTBGTneVv85iYpRcZCMuZCFsFRsvcxy9sK6pkCcmrInQjcgWQuYdoWWurFcVGfArJi3grBUKYtc36MSs6Itae6TEv8W1jrOvcZApqG5dXbi3RZBwFbS9ZCCtqqtrg61H2mu6YllCL2FbJ74OFl6'}
	user_details = requests.get(user_details_url, user_details_params).json()
	# pprint(user_details)
	if response['entities']:
		text=str(response['_text'])
		text=cleaning_text(text)
		intent_type= response['entities']['intent'][0]['value']      #Storing intent type for user interactions for different intents.
		if intent_type == 'greet':
			text="Hey " + str(user_details['first_name']) + "! This is hackRush :) . I can remind you stuff, intimate you about your medicines without any input from you, track the PNR status of your train booking, train availability, etc. Though I am still young and in development stage , but I am a fast learner ;) . I will try to learn more things to become more useful for you B-)"
			greet_post_fb(fb_id,text)
			# data={"fromcode":"BOM","fromname":"Bombay","tocode":"AHM","toname":"Ahmedabad","pnr":"102981244","status":"confirm","train":{"number":"191111"}}
			# prescribe_post_fb('9909986189',fb_id)
		elif intent_type == 'prescription':
			prescribe_post_fb('2830910360256187',fb_id)
		elif intent_type=='weather':
			askLocation(fb_id)
		elif intent_type=='reminder':
			event = response['entities']['event'][0]['value']
			date = response['entities']['datetime'][0]['value']
			reminder_fun(fb_id, event, date)
		elif intent_type=='check_pnr':
			pprint(response['entities'])
			pnrno = int(response['entities']['pnr_number'][0]['value'].strip())
			apikey = '6e3wxyk07x'
			l2='https://api.railwayapi.com/v2/pnr-status/pnr/{}/apikey/{}/'.format(pnrno,apikey)
			print(l2)
			res = requests.get(l2)
			print(res.text)
			json_data = json.loads(res.text)
			pprint(json_data)
			from_sta=json_data['boarding_point']['name']+' '+'('+json_data['boarding_point']['code']+')'
			to_sta=json_data['reservation_upto']['name'] + ' ' + '(' + json_data['reservation_upto']['code'] + ')'
			train_details=json_data['train']['name'] + ' ' + '(' + json_data['train']['number'] + ')'
			status=json_data['passengers']
			li=from_sta+'\n'+to_sta+'\n'+train_details+'\n'
			for i in status:
				for j in i:
					li+=str(j)+' : '+str(i[j])+'\t'
				li+='\n'
			master_post_fb(fb_id,li)
		elif intent_type=='journey':
			#source_station    destination_station
			try:
				start_str = response['entities']['source_station'][0]['value']
				to_str = response['entities']['destination_station'][0]['value']
				dmy = str(datetime.datetime.now().day)+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().year)
				print(dmy)
				apikey = '6e3wxyk07x'
				lin1='https://api.railwayapi.com/v2/suggest-station/name/'+start_str+'/apikey/'+str(apikey)+'/'
				lin2 = 'https://api.railwayapi.com/v2/suggest-station/name/'+to_str+'/apikey/' + str(apikey) + '/'
				response1 = requests.get(lin1)
				response2 = requests.get(lin2)
				json_data1 = json.loads(response1.text)
				json_data2 = json.loads(response2.text)
				st='Sorry :( ,  No station found.'
				flag=0
				if len(json_data1['stations'])>0 and len(json_data2['stations'])>0:
					src_code=json_data1['stations'][0]['code']
					dest_code=json_data2['stations'][0]['code']
				l4='https://api.railwayapi.com/v2/between/source/{}/dest/{}/date/{}/apikey/{}/'.format(src_code,dest_code,dmy,apikey)
				response=requests.get(l4)
				json_data=json.loads(response.text)
				jeff=json_data['trains'][0]
				strin=''
				strin+='Train Number' +': '+ str(jeff['number'])+'\n'
				strin += 'Train Name' + ': ' + str(jeff['name']) + '\n'
				strin += 'Travel Time' + ': ' + str(jeff['travel_time']) + '\n'
				strin += 'Src Depart Time' + ': ' + str(jeff['src_departure_time']) + '\n'
				strin += 'Dest Arrival Time' + ': ' + str(jeff['dest_arrival_time']) + '\n'
				strin += 'From Station ' + ': ' + str(jeff['from_station']['name'])+' ('+str(jeff['from_station']['code']) +') ' + '\n'
				strin += 'To Station ' + ': ' + str(jeff['to_station']['name'])+' ('+str(jeff['to_station']['code']) +') ' + '\n'
				strin += 'Classes:\n'
				for i in jeff['classes']:
				    for j in i:
				        strin+=' ' + j + ': ' + str(i[j]) + '\t'
				    strin += '\n'
				strin += 'Running days:\n'
				for i in jeff['days']:
				    strin+=i['code']+'('+i['runs']+')'+'\t'		
				master_post_fb(fb_id,strin)
			except:
				master_post_fb(fb_id,":( Sorry! No Trains found")		
				return HttpResponse()											
		else:
			master_post_fb(fb_id,text)
	else:
		default_text="\nSorry, I don't Understand. Please retry some other value!! :("
		master_post_fb(fb_id,default_text)

actions = {
    'send': send,
}
# client=Wit(access_token=wit_access_token,actions=actions)
client=Wit(wit_access_token)