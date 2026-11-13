from codec_core import decode


def run(payload):
    cache={}
    output=[]
    for code in payload['codes']:
        if code not in cache:
            cache[code]=decode(code)
        output.append(cache[code])
    return output
