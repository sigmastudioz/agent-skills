def run(payload):
    index={row['tenant']+':'+row['key']:row['value'] for row in payload['rows']}
    return [index.get(tenant+':'+key) for tenant,key in payload['queries']]
