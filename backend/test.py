import urllib.request, json
req = urllib.request.Request('http://localhost:8000/api/chat', data=b'{"query":"how do I get help"}', headers={'Content-Type':'application/json'})
try:
    print(urllib.request.urlopen(req).read().decode('utf-8'))
except Exception as e:
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
    else:
        print(e)
