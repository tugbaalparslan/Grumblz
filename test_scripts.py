import http.client

conn38- = http.client.HTTPSConnection("http://127.0.0.1:5001")
payload = "{\"name\": \"Tugba\", \"last_name\": \"Alparslan\", \"phone\": \"9495016315\", \"gender\": \"Female\"}"
headers = {
  'Content-Type': 'application/json'
}
conn.request("POST", "/user/<email>", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))