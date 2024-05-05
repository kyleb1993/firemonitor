import http.client, urllib, time
conn = http.client.HTTPSConnection("api.pushover.net:443")

conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": "pushover api token",
    "user": "pushover user token",
    "message": "System Normal: Fire Alarm Restored",
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()
