
import os
import urllib3
import json

def lambda_handler(event, context):
    print(event)
    webhook_url = "https://hooks.slack.com/services/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"

    message = """
        {title}
        *Database*: {database}  
        *Table*: {table} 
        *Status*: {status}
        """.format(
        title=":red_circle: Task Failed." if event['Query']['Status'] == 'FAILED' else ":large_green_circle: Task Succeeded.",
        database=event['database'],
        table=event['table'],
        status=event['Query']['Status']
        
    )
    
    http = urllib3.PoolManager()
    r = http.request(
        'POST',
        webhook_url,
        headers={'Content-Type': 'application/json'},
        body=json.dumps({'text': message})
    )
    print(r.data)
    return r.data

     