import json

def lambda_handler(event, context):
    print(event)
    event['waitSeconds']=event['waitSeconds']*2
    return event
