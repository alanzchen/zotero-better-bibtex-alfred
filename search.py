#!/usr/bin/python
# encoding: utf-8

import sys
import requests
import json

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3


def main(wf):
    # The Workflow3 instance will be passed to the function
    # you call from `Workflow3.run`.
    # Not super useful, as the `wf` object created in
    # the `if __name__ ...` clause below is global...
    #
    # Your imports go here if you want to catch import errors, which
    # is not a bad idea, or if the modules/packages are in a directory
    # added via `Workflow3(libraries=...)`

    # Get args from Workflow3, already in normalized Unicode.
    # This is also necessary for "magic" arguments to work.
    args = wf.args

    # Do stuff here ...

    # Add an item to Alfred feedback
    keyword = args[0]
    r = search(keyword)
    for i in r:
        try:
            authors = [j['family'] for j in i['author']]
            authors_ = ', '.join(authors)
        except KeyError:
            authors_ = 'Missing Authors'
        year = ''
        try:
            year = str(i['issued']['date-parts'][0][0]) + ' '
        except KeyError:
            pass
        wf.add_item(i['title'], year + authors_, arg='@' + i['citekey'], valid=True)

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    wf.send_feedback()


def search(keyword):
    # cURL
    # POST http://localhost:23119/better-bibtex/json-rpc

    try:
        response = requests.post(
            url="http://localhost:23119/better-bibtex/json-rpc",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "jsonrpc": "2.0",
                "method": "item.search",
                "params": [
                    keyword
                ]
            })
        )
        return response.json()['result']
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))
