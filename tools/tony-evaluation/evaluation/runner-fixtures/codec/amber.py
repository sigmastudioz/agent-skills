from codec_core import decode


TABLE=[decode(code) for code in range(16384)]


def run(payload):
    return [TABLE[code] for code in payload['codes']]
