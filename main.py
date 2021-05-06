import requests
import time
import json
from os import system
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime,timedelta
clear = lambda:system('cls')
#msg = """""" #empty message
send_details = False
tomorrow = datetime.now() + timedelta(days=1)
date = tomorrow.strftime("%d-%m-%Y")
def send_email(msg):
    port = 465 #for ssl encryption
    smtp_server = "smtp.gmail.com"
    sender_email = "sender_email" #dont use your primary address because of security issues
    # Go to google settings and enbale "allow less secure apps" to send email with code
    sender_password = "sender_password" # or chose input function to enter password
    receiver_email = "receiver_email" #if many, make some change in code and send msg with loop
    message = MIMEMultipart('alternative')
    message["Subject"] = "covid vaccine registration portal details(Bot Generated) "
    message["From"] = sender_email
    message["To"] = receiver_email
    text = """\
    Unable to send report
    """ #this is an odd case only for which that doesn't support html format
    html = f"""\
    <html>
    <head>
        <style>
            table, th, td {{border:1px solid black;}}
        </style>
    </head>
    <body>
        <table>
            <tr>
                <th>NAME</th>
                <th>BLOCK NAME</th>
                <th>PINCODE</th>
                <th>FEE TYPE</th>
                <th>AVAILABLE CAPACITY</th>
                <th>MINIMUM AGE LIMIT</th>
                <th>DATE</th>
            </tr>
            {msg}
        </table>
    </body>
    </html>
    """
    part1 = MIMEText(text,"plain")
    part2 = MIMEText(html,"html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server,port,context=context) as server:
        server.login(sender_email,sender_password)
        server.sendmail(sender_email, receiver_email,message.as_string())
        print(f"Email send successfully to {receiver_email}")
def findLoc(send_details):
    # id = 297 for kannur !
    #creating empty msg
    availableCapacityMsg = ""
    minAgeLimitMsg = ""
    dateMsg = ""
    try:
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=297&date={date}"
    except Exception as e:
        print("exception occured in url \n",e)
        exit()
    headers = {
    "accept-encoding": "gzip, deflate, br",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    }
    res = requests.get(url,headers=headers)
    #create a file called 'file.json' in the current directory by yourself to store the response
    with open("file.json","wb") as f:
        f.write(res.content)
    f = open("file.json","r")
    try:
        data = json.load(f)
    except Exception as e:
        print(e)
        print("Unauthenticated access!")
        exit()
    msg = '''''' # initialised empty multiline messge
    if data["centers"] != []: #if not null
        for center in data["centers"]:
            msg += f'''<tr><td>{center["name"]}</td><td>{center["block_name"]}</td><td>{center["pincode"]}</td><td>{center["fee_type"]}</td>'''
            #printing whole centers
            print("AVAILABLE CENTERS \n****************")
            print("name: " ,center["name"])
            print("block name: ",center["block_name"])
            print("pincode: ",center["pincode"])
            print("fee type: ",center["fee_type"])

            for session in center["sessions"]:
                print("available capacity: ",session["available_capacity"])
                print("minimum age limit: ",session["min_age_limit"])
                print("date: ",session["date"])
                availableCapacityMsg += f"{session['available_capacity']} "
                minAgeLimitMsg +=f"{session['min_age_limit']} "
                dateMsg += f"{session['date']} "
            msg += f"""<td>{availableCapacityMsg}</td><td>{minAgeLimitMsg}</td><td>{dateMsg}</tr>"""

            print("\n")
            if center["pincode"] in [670591,670592]: #To get mail only for the closest one. Otherwise it won't send me the email containg list. You can add pincode near to your place
                send_details = True
        # print(msg) #remove comment only if want to display msg html code
        try:
            if send_details == True:
                send_email(msg)
                send_details = False
                print(f"Since pincode found , waiting for 15 minutes({60*15} seconds)")
                time.sleep(60 * 15) #sleeping for 15 minutes to prevent continuesly sending mail
            else:
                print("Message didn't send")
        except Exception as e:
            print(e)
    else:
        print(res.status_code ,"\nSomething went wrong ! unable to get response")
    f.close()

# main
while True:
    findLoc(send_details)
    time.sleep(10) #sleep for 10 seconds to make the next https request
    try:
        clear() #clear the terminal to get neat look
    except:
        pass
