import requests
import time
import smtplib
import ssl
import logging


# An HTTP GET request is made to ASU course catalog API and if successful, returns a JSON object for course CSE 412.
def get_classes():
    # The headers were copied from Firefox Web Developer Tools.
    headers = {
        'host' : 'eadvs-cscc-catalog-api.apps.asu.edu',
        'user-agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'accept' : '*/*',
        'accept-language' : 'en-US,en;q=0.5',
        'accept-encoding' : 'gzip, deflate, br',
        'referer' : 'https://catalog.apps.asu.edu/',
        'authorization' : 'Bearer null',
        'origin' : 'https://catalog.apps.asu.edu',
        'connection' : 'keep-alive',
        'cookie' : '_ga_TEHJR60KD9=GS1.1.1689107861.8.1.1689107880.41.0.0; _ga=GA1.2.1401611855.1688429277; _ga_4C79928C5X=GS1.2.1689107863.7.1.1689107887.0.0.0; asuCookieConsent=true; _gcl_au=1.1.2124630252.1688432764; _hjSessionUser_2572449=eyJpZCI6ImNjYjg5OTkzLTFhMjYtNTljNi05ZTg3LTMxOTAzNmFhNTE3OCIsImNyZWF0ZWQiOjE2ODg0MzI3NjUyMzAsImV4aXN0aW5nIjpmYWxzZX0=; FPAU=1.1.2124630252.1688432764; _fbp=fb.1.1688432765994.1821302948; __gsas=ID=e72f625ca9a4323e:T=1688432778:RT=1688432778:S=ALNI_MbJjKfpI6DmuixGJZk-6XGTkPimRQ; _gid=GA1.2.145746085.1689107862; _gat=1; _gat_UA-42798992-4=1',
        'sec-fetch-dest' : 'empty',
        'sec-fetch-mode' : 'cors',
        'sec-fetch-site' : 'same-site' }

    url = 'https://eadvs-cscc-catalog-api.apps.asu.edu/catalog-microservices/api/v1/search/classes?=&refine=Y&campusOrOnlineSelection=A&catalogNbr=412&honors=F&promod=F&searchType=all&subject=CSE&term=2237'

    r = requests.get(url, headers=headers)

    return (r.json())


# Seating information of course CSE 412 is extracted from JSON data from get_classes().
def check_cap():
    j = get_classes()
    classes = j['classes']

    x = classes[0]
    y = classes[1]

    a = x['seatInfo']
    b = y['seatInfo']
    
    if (a['ENRL_TOT'] < 160) or (b['ENRL_TOT'] < 160):
        check = True
    else:
        check = False

    return check


# Using SMTP, an email is sent with Outlook once a seat in course CSE 412 is available.
def email_bot():
    sndr = 'sender@email.com'
    recp = 'recipient@email.com'
    pswrd = 'Password'

    txt = 'From: %s\r\nTo: %s\r\n\r\n412 seat open' % (sndr, recp)

    cntxt = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.ehlo()
        server.starttls(context=cntxt)
        server.ehlo()
        server.login(sndr, pswrd)

        server.sendmail(sndr, recp, txt)


# Every 15 minutes check_cap() is called. If there is an open seat for course CSE 412, an email is sent and exits.
def main():
    isOpen = False

    while (not isOpen): 
        isOpen = check_cap()

        if (isOpen):
            logging.info('412 seat open')
            email_bot()
        else:
            logging.info('412 seat not open')
            time.sleep(900)


if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)

    main()