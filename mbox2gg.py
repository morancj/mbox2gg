#! /usr/bin/env python

# Import a mbox file to a Google Group using https://developers.google.com/admin-sdk/groups-migration/index
# You'll need to install https://developers.google.com/api-client-library/python/
# and enable Groups Migration API, read prerequisits of the API SDK



import mailbox
import io
import time

import apiclient
import httplib2
from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# The email address of the group to import to
groupId = input('Enter groupId: ')

# https://console.developers.google.com/project/mysociety-groups-import/apiui/credential
# Generate a Client ID for Native Application.
# You'll be prompted to complete an auth flow on the first run.
# The user will need to be an admin.
scope = 'https://www.googleapis.com/auth/apps.groups.migration'

storage = Storage('credentials.dat')

credentials = storage.get()

if not credentials or credentials.invalid:
    client_id = input('Enter client_id: ')
    client_secret = input('Enter client_secret: ')
    flow = client.OAuth2WebServerFlow(client_id, client_secret, scope)
    if flags:
        credentials = tools.run_flow(flow, storage, flags)
    else:
        # Needed only for compatibility with Python 2.6
        credentials = tools.run(flow, storage)

http = credentials.authorize(httplib2.Http())

service = discovery.build('groupsmigration', 'v1', http=http)

mbox_path = input('Enter mbox_path: ')

mb = mailbox.mbox(mbox_path)  # The path of the mbox file to import

i = 1
total_messages = len(mb)

for msg in mb:
    stream = io.StringIO()
    stream.write(msg.as_string())
    message_size = msg.as_string().__sizeof__()
    if message_size >= 26214400:
        print('Message {} - Size {} - subject : {}'.format(i, message_size, msg['subject']))
        continue
    media = apiclient.http.MediaIoBaseUpload(
        stream, mimetype='message/rfc822')
    response = service.archive().insert(
        groupId=groupId, media_body=media).execute()

    print('Message {} of {}: {}'.format(
        i,
        total_messages,
        response['responseCode'])
    )

    i = i + 1

    time.sleep(1)

print('Done.')
