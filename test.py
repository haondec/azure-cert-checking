import csv
import json

json_file = open("sample.json", "r")

parse_data = json.load(json_file)


fieldnames = ['cert_name', 'status', 'expiration_date']
certs_csv_writer = csv.DictWriter(open('cert_list.csv', mode='w'), fieldnames=fieldnames)
certs_csv_writer.writeheader()

crt = dict()

crt['cert_name'] = parse_data[0]['name']
crt['status'] = parse_data[0]['properties']['status']
crt['expiration_date'] = parse_data[0]['properties']['expirationTime']

certs_csv_writer.writerow(crt)

certs_csv_writer.writerow(crt)