def run(payload):
    index={}
    for row in payload['rows']:
        index.setdefault((row['tenant'],row['key']),row['value'])
    return [index.get((tenant,key)) for tenant,key in payload['queries']]
