from codec_core import decode


def run(payload):
    return [decode(code) for code in payload['codes']]
