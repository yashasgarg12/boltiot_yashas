import email_conf
from boltiot import Email, Bolt
import json, time

minimum_limit = 0 #the minimum threshold of temp value 
maximum_limit = 81.92 #the maximum threshold of temp value 
print("Min Limit: "+str(minimum_limit)+"\nMax Limit: "+str(maximum_limit))

mybolt = Bolt(email_conf.API_KEY, email_conf.DEVICE_ID)
mailer = Email(email_conf.MAILGUN_API_KEY, email_conf.SANDBOX_URL, email_conf.SENDER_EMAIL, email_conf.RECIPIENT_EMAIL)


while True: 
    response = mybolt.analogRead('A0') 
    data = json.loads(response) 
    print ("Sensor value is: " + str(data['value']))
    try: 
        sensor_value = int(data['value']) 
        if sensor_value > maximum_limit or sensor_value < minimum_limit:
            print("Making request to Mailgun to send an email")
            response = mailer.send_email("Alert", "The Current temperature sensor value is " +str(sensor_value))
            response_text = json.loads(response.text)
            print("Response received from Mailgun is: " + str(response_text['message']))
    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(10)
