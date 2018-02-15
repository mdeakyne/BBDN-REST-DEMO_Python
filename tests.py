payload = {
    "objectType": 'courses',
    "externalId": 'ENC1101-123456',
    "dataSourceId": 'externalId:20164',
    "objectId": '_123_1',
    "name": "Course used for REST demo",
    "description": "Course used for REST demo",
    "allowGuests": "true",
    "readOnly": "false",
    "availability": {
        "duration": "continuous"
    }
}

payload.get('availability').update({'available': 'Yes'})
print(payload)
