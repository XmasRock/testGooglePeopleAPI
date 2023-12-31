import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/contacts']

def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('people', 'v1', credentials=creds)

        # Call the People API 
        print('>>>>>>>> List 10 connection names')
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='names,emailAddresses').execute()
        #print(str(results))
        connections = results.get('connections', [])        
        for data in connections:
            for email in data["emailAddresses"]:
                print("\t" + email["value"])


        # Call the People API to add a new contact
        # Contact data structure : https://developers.google.com/resources/api-libraries/documentation/people/v1/python/latest/people_v1.people.html
        print('\n >>>>>>>> Add  new contact John Duschmol')
        new_contact = {
                    'names': [
                        {
                            'displayName': 'John Duschmol'
                        }
                    ],
                    'emailAddresses': [
                        {
                            'value': 'john.duschmol@temlab.fr',
                            "type": "home"
                        }
                    ],
                    "addresses": [
                        { 
                        "city": "Courgent",
                        "countryCode": "FR",
                        "region": "Yvelines, Ile de France",
                        "poBox": "26",
                        "streetAddress": "rue des Grouettes",
                        "country": "France",
                        "postalCode": "78790",
                        "type": "work"
                        }
                    ],
                    "phoneNumbers": [
                        {
                        "type": "work",
                        "value": "+33766886312",
                        "metadata": {"primary": True},
                        },
                        {
                        "type": "home",
                        "value": "+33766886312",
                        "metadata": {"primary": False},
                        },
                    ]
                }
        result = service.people().createContact(body=new_contact).execute()
        print('\n>>>>>>>>New Contact created >>>', result)

        #
        # --- now delete this new entry
        #
        resourceName = result['resourceName']
        print("\n>>>>>>>> DELETE ResourceName  " + resourceName)
        result = service.people().deleteContact(resourceName=resourceName)

    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()

