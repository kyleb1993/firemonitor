import http.client, urllib
conn = http.client.HTTPSConnection("api.pushover.net:443")

conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": "pushover api token",
    "user": "pushover user token",
    "message": "System Trouble",
    "priority": "1",
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()
