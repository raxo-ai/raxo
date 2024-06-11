import re
from json import loads


def find_between_braces(sentence):
    """gets all the text between the braces"""
    resp = sentence
    match = re.search(r'\{(.*)\}', sentence)
    try:
        if match:
            resp = '{' + match.group(1) + '}'
            resp = re.sub("\'", '\"', resp)
            resp = resp.replace("None", "null")
            resp = loads(resp)
    except Exception as e:
        e = str(e)
    return resp


def extract_output(response):
    """extracts the output from gpt response"""
    try:
        resp = loads(response)
    except Exception as e:
        e = str(e)
        resp = find_between_braces(response)
    return resp
