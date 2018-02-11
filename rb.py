import rebooter
import rball
import os
import sys
import time
import urllib, urllib2, json, requests
import textwrap
import string
import random
import datetime
from slackclient import SlackClient

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

slack_token = ''
sc = SlackClient(slack_token)

def slackmessage(m):
    sc.api_call(
      "chat.postMessage",
      channel="#rigstatus",
      text=m,
      as_user="False",
      username=user,
    )

def delete_last_lines(n=1):
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)

def minerStatus(rig):
	status = str(data['rigs'][rig]['condition'])
	if status == 'mining':
		x = status.replace('mining', 'OK      ')
	elif status == 'stuck_miners':
		x = status.replace('stuck_miners', 'STUCK   ')
	elif status =='just_booted':
		x = status.replace('just_booted', 'BOOTUP  ')
	elif status == 'unreachable':
		x = status.replace('unreachable', 'D/C     ')
	elif status == 'overheat':
		x = status.replace('overheat', 'HEAT    ')
	elif status == 'no_hash':
		x = status.replace('no_hash', 'NO HASH ')
	else:
		x = status
	return x

def minerGPUs(rig):
	status = str(data['rigs'][rig]['miner_instance'])
	return status

def print_slow(typeout):
    for letter in typeout:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.045)

def print_slower(typeout):
    for letter in typeout:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.15)

def hashrateMod(hashrate):
	hr = hashrate
	#hr = int((data['per_info']['claymore']['hash']))
	if hr > 1000:
		x = str(hr) + "  "
	elif hr > 100:
		x = str(hr) + "  -"
	elif hr > 10:
		x = str(hr) + "  --"
	elif hr >= 0:
		x = str(hr) + "  ---"
	return x 

i = 60
rig = ''
riggo = ''
rigga = ''

while True:
	os.system('clear')
	print("    ---------------------------------------------")
	print("    |-----------  RIG PANEL v0.1.6  ------------|")
	print("    |-------------------------------------------|")
	print("")
	print("    Enter User Number:")
	print("    [1] Freak")
	print("    [2] Weeze")
	print("")
	uin = raw_input("====> ")

	if uin == '1':
		user = 'Freak'
		break
	elif uin == '2':
		user = 'Weeze'
		break
	else:
		print('    Enter 1 or 2')
		time.sleep(2)

while True:
	try:
		os.system('clear')
		ret = urllib2.urlopen(urllib2.Request('http://vega07.ethosdistro.com/?json=yes'))
		data = json.loads(ret.read())
		hashrate = int((data['per_info']['claymore']['hash']))
		print("    ---------------------------------------------")
		print("    |-----------  RIG PANEL v0.1.6  ------------|")
		print("    |---------------  HR: " + str(hashrateMod(hashrate)) + "----------------|")
		print("    |            Logged in as " + user + "             |")
		print("    |                                           |")
		print("    |  A1 Status: " + minerStatus('5026ef') + "|  " + minerGPUs('5026ef') + "/7 GPUs Running   |")
		print("    |  A2 Status: " + minerStatus('50270d') + "|  " + minerGPUs('50270d') + "/7 GPUs Running   |")
		print("    |  A3 Status: " + minerStatus('482892') + "|  " + minerGPUs('482892') + "/9 GPUs Running   |")
		print("    |  B1 Status: " + minerStatus('502b8a') + "|  " + minerGPUs('502b8a') + "/9 GPUs Running   |")
		print("    |  B2 Status: " + minerStatus('590b29') + "|  " + minerGPUs('590b29') + "/8 GPUs Running   |")
		print("    |-------------------------------------------|")
		while i > 0:
			print("    |   Input: ctrl + c   |   Refresh: " + str(datetime.timedelta(seconds=i)) + "  | \r")
			print("    ---------------------------------------------")
			delete_last_lines(2)
			time.sleep(1)
			i -= 1
		i = 60

	except KeyboardInterrupt:
		i = 60
		print("  | Reboot single Rig: a1, a2, etc.           |")
		print("    | Reboot all rigs  : all                    |")
		print("    | ENTER (no command) for manual update      |")
		print("    | Q to quit back to terminal                |")
		print("    ---------------------------------------------")
		riggo = raw_input("====>  Panel Command: ")
		rig = riggo.upper()
	
		if rig == 'A1' or rig == 'A2' or rig == 'A3' or rig == 'B1' or rig == 'B2':
			s = raw_input('Send message to slack channel? (y/n) ')
			if s == 'y':
				slackmessage("Rebooting " + rig)
			rebooter.rebme(rig)
	
		elif rig == 'Q':
			print('Exiting...')
			sys.exit(0)
	
		elif rig == 'ALL':
			s = raw_input('Send message to slack channel? (y/n) ')
			if s == 'y':
				slackmessage("Rebooting ALL")
			rball.rbooter()
	
		elif rig == 'DADJOKE':
			response = requests.get("https://icanhazdadjoke.com/",
  		  		headers={
    	    		"Accept": "application/json"
  		  		}
			)
			print textwrap.fill(response.json()['joke'], 40)
			print('')
			raw_input("Press enter to return...")

		elif rig == 'ACCESS MAIN PROGRAMMING':
			sys.stdout.write("        ")
			sys.stdout.flush()
			print_slow("Ah ah ah!")
			time.sleep(1.1)
			sys.stdout.write("  ")
			print_slow("You didn't say the magic word!")
			time.sleep(3)

		elif rigga == '' or riggo == '':
			print('')
			sys.stdout.write('     Updating')
			sys.stdout.flush()
			print_slower('.....')
			time.sleep(2)

		else:
			print("")
			print("    " + riggo + "ed your mom last night")
			time.sleep(3)

	i = 60