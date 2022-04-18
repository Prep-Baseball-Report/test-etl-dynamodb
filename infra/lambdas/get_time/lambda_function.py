from datetime import datetime, timedelta

def lambda_handler(event, context):
    if not event.get('backfill_timestamp'):
            timestamp = datetime.utcnow() - timedelta(hours = 2)
            timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    else:
        timestamp = event['backfill_timestamp']
    return timestamp