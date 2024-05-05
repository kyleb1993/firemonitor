import http.client, urllib
conn = http.client.HTTPSConnection("api.pushover.net:443")

conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": "pusheover api token",
    "user": "pushover user token",
    "message": "Fire Alarm Active",
    "priority": "2",
    "retry": "30",
    "expire": "3600",
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()

