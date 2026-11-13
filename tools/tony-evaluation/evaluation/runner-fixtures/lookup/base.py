def run(payload):
    output=[]
    for tenant,key in payload['queries']:
        value=None
        for row in payload['rows']:
            if row['tenant']==tenant and row['key']==key:
                value=row['value']
                break
        output.append(value)
    return output
