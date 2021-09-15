#!/usr/bin/python3
# Haond checking Azure cert

import adal
import requests
import os
import json
import csv
import smtplib, ssl
from datetime import datetime

#-----------------------------------------------------------------
# Setting SMTP gmail
sendmail_enable = False
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = ""
receiver_email = ""
password = ""
message = "Subject: [Azure] Certificate expired warning\n\n"

# Setting Azure
# Tenant ID (Active directory)
tenant = os.environ['TENANT']
# App registrations (client) ID
client_id = os.environ['CLIENT_ID']
# App registrations -> Certificate & secrets -> Client secret
client_secret = os.environ['CLIENT_SECRET']
# Subscription ID
subscription_id = os.environ['SUBSCRIPTION_ID']

# Setting day remaining to alert
date_remaining = 90
#-----------------------------------------------------------------
# Create CSV
fieldnames = ['cert_name', 'status', 'expiration_date']
certs_csv_writer = csv.DictWriter(open('cert_azure_list_warning.csv', mode='w'), fieldnames=fieldnames)
certs_csv_writer.writeheader()
# Create dictionary
row_crt = dict()

# Resouce
resource = 'https://management.azure.com/'
# Authority URL to get token/bearer
authority_url = 'https://login.microsoftonline.com/' + tenant
context = adal.AuthenticationContext(authority_url)
# Get token/bearer
token = context.acquire_token_with_client_credentials(resource, client_id, client_secret)

# Request GET
headers = {'Authorization': 'Bearer ' + token['accessToken']}
params = {'api-version': '2019-08-01'}
url = 'https://management.azure.com/subscriptions/' + subscription_id + '/providers/Microsoft.CertificateRegistration/certificateOrders'
# Run GET
r = requests.get(url, headers=headers, params=params)

# Dump data json after GET
data = json.dumps(r.json(), indent=4, separators=(',', ': '))

# Parse data
parse_data = json.loads(data)

# Function zone
def days_between_now(d):
    date_now = datetime.now()
    date_object = datetime.strptime(d[0:10], "%Y-%m-%d")
    return (date_object - date_now).days
# end

# Checking cert expired
list_expired = []
list_warning = []
for i in range(len(parse_data['value'])):
    # Uncheck cert invalid
    if 'properties' not in parse_data['value'][i]:
        continue
    if 'expirationTime' not in parse_data['value'][i]['properties']:
        continue
    # Get date expired
    date_expired = parse_data['value'][i]['properties']['expirationTime']
    status = parse_data['value'][i]['properties']['status']
    cert_name = parse_data['value'][i]['name']
    # Write CSV
    row_crt['cert_name'] = cert_name
    row_crt['status'] = status
    row_crt['expiration_date'] = date_expired
    certs_csv_writer.writerow(row_crt)

    diff_day = days_between_now(date_expired)
    if diff_day <= 0:
        list_expired.append(i)
        continue
    if diff_day <= date_remaining:
        list_warning.append(i)
        continue

# Generate message
if len(list_expired) == 0 and  len(list_warning) == 0:
    print("No cert expired or nearly expiring.")
    exit()

# List expired
out = "List expired: " + str(len(list_expired))
message += out + "\n"
# Console out
for i in list_expired:
    out = "- App Certificate: " + parse_data['value'][i]['name'] + " | " + parse_data['value'][i]['properties']['expirationTime']
    message += out + "\n"

# List warning
out = "List warning: " + str(len(list_warning))
message += out + "\n"
print(out)
for i in list_warning:
    diff_day = days_between_now(parse_data['value'][i]['properties']['expirationTime'])
    out = "- App Certificate: " + parse_data['value'][i]['name'] + " | " + parse_data['value'][i]['properties']['expirationTime'] + " | " + str(diff_day) + " days remaining"
    message += out + "\n"

# Send mail
if sendmail_enable:
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
