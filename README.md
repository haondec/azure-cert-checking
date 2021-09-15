# Script fetch Cert information in AZ-Subscription

## Ref

* Explain resource manager [link](https://lnx.azurewebsites.net/azure-resource-manager-api-calls-from-python/)
* SDK list [link1](https://docs.microsoft.com/en-us/rest/api/appservice/certificates/list) [link2](https://github.com/Azure/azure-sdk-for-python)
* SDK test [link](https://docs.microsoft.com/en-us/rest/api/appservice/appservicecertificateorders/list?view=azurecosmosdbcfp-1.0.0#code-try-0)

## Concept

```doc
- Client ID is an Application ID you created for RBAC (as described here). This is the AAD Application with a Service Principal object related to it.

- Client Secret is an AAD Application's key (password).

- Tenant ID is your AD Tenant's ID you can find in AAD Properties or in output of the az ad sp create-for-rbac command.

- Resource is https://management.azure.com/ - Azure Resource Manager provider APIs URI.

- Authority URL is https://login.microsoftonline.com/ - the Identity Provider address.

- API version is a query-string parameter with designated API version you should provide for service you are calling. You can find this parameter in API reference under provider of choice - here an example for Resource Management / Resource Groups / List.
```

---

## Setup

### Install requirements

```bash
pip3 install requests adal
```

### Declare variable OS

```bash
TENANT=xxxx
CLIENT_ID=xxxx
CLIENT_SECRET=xxxx
SUBSCRIPTION_ID=xxxx
```

### To use email notify, in script

```python3
# Setting SMTP gmail
sendmail_enable = False
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = ""
receiver_email = ""
password = ""
message = "Subject: [Azure] Certificate expired warning\n\n"
```

### Update the number day want to check, in script

```python3
date_remaining = 90
```

### Run script

```bash
python3 azcertcheck_appservice_v2.py
```
