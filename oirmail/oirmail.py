from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import httplib2
import os
import csv

from apiclient import discovery, errors
import oauth2client
from oauth2client import client
from oauth2client import tools

from email.mime.text import MIMEText

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


__author__ = 'S. May'

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_threadsbylabels(service, user_id, label_ids=[]):
    """List all Threads of the user's mailbox with label_ids applied.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        label_ids: Only return Threads with these labelIds applied.

    Returns:
        List of threads that match the criteria of the query. Note that the returned
        list contains Thread IDs, you must use get with the appropriate
        ID to get the details for a Thread.
    """
    try:
        response = service.users().threads().list(userId=user_id,
                                                  labelIds=label_ids).execute()
        threads = []
        if 'threads' in response:
            threads.extend(response['threads'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().threads().list(userId=user_id,
                                                    labelIds=label_ids,
                                                    pageToken=page_token).execute()
            threads.extend(response['threads'])

        return threads

    except errors.HttpError, error:
        print('An error occurred: %s' % error)

def get_thread(service, user_id, thread_id): 
    """ Get a thread with thread_id. 
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        thread_id: The ID of the Thread required.

    Returns:
        Thread with matching ID.
    """
    try:
        thread = service.users().threads().get(userId=user_id, id=thread_id).execute()
        messages = thread['messages']
        return thread

    except errors.HttpError, error:
        print('An error occurred: %s' % error)

def get_message(service, user_id, msg_id):
    """Get a Message with given ID.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.
    Returns:
        A Message.
    """
    try:
        return service.users().messages().get(userId=user_id, id=msg_id).execute()
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

def get_label(service, user_id, label_id): 
    """Get a Label with given ID. 
    Args: 
        service: Authorized Gmail API service instance.
        user_id: Users's email address. the special value "me" can be used
        to indicate teh autenticated user.
        msg_id: The ID of the Label required.
    """
    try: 
        return service.users().labels().get(userId=user_id, id=label_id).execute()
    except errors.HttpError, error: 
        print('An error occured: %s' % error)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main(mail_label):
    """
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    profile = service.users().getProfile(userId='me').execute()
    email = profile["emailAddress"]

    # labels are not allowed to have the same name (even lower or upper)
    for label in labels: 
        if label['name'].lower() == mail_label.lower(): 
            label_id = label['id']

    try: 
        threads = get_threadsbylabels(service, user_id='me', label_ids=[label_id])
    except Exception: 
        print("Label not found")

    m_id_list = []
    headers = ["thread_id", "message_id", "labels", "date", "to", "from", "subject", "snippet"]
    write_headers = True
    
    if os.path.isfile("output.csv"): 
        with open("output.csv", 'r') as o_rd: 
            rd_output = csv.reader(o_rd)
            prev_list = list(rd_output)
            m_id_index = headers.index("message_id")
            m_id_list = [prev_list[i][m_id_index] for i in xrange(1, len(prev_list))]
            write_headers = False

    output_write = open('output.csv', "a+")
    wt_output = csv.writer(output_write)

    if write_headers:
        wt_output.writerow(headers)


    for thread in threads: 

        t = get_thread(service, user_id='me', thread_id=thread['id'])
        messages = t['messages']

        for message in messages: 
            if message['id'] not in m_id_list: 

                m = get_message(service, user_id='me', msg_id=message['id'])
                print("ADDING MESSAGE TO LOG: id =", message['id'])

                for dct in m['payload']['headers']:
                    if dct['name'] == 'Date': 
                        date = dct['value']
                    elif dct['name'] == 'To':
                        to = dct['value']
                    elif dct['name'] == 'From':
                        fr = dct['value']
                    elif dct['name'] == 'Subject': 
                        subj = dct['value']
                label_list = []
                for l in m['labelIds']: 
                    label_list.append(get_label(service, user_id='me', label_id=l)["name"])
                label_string = ', '.join(label_list)

                row = [m['threadId'], m['id'], label_string, date, to, fr, subj, m['snippet']]
                wt_output.writerow(row)

    print("DONE.")

        


if __name__ == '__main__':
    mail_label = raw_input('Provide the name of the gmail label: ')
    #user_name = raw_input('Please provide your email address: ')
    main(mail_label)







