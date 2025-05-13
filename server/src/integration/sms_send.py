# Looking to send emails in production? Check out our Email API/SMTP product!
import requests

url = "https://sandbox.api.mailtrap.io/api/send/3163160"

payload = "{\"from\":{\"email\":\"hello@example.com\",\"name\":\"Mailtrap Test\"},\"to\":[{\"email\":\"tolgabayrakj@gmail.com\"}],\"subject\":\"You are awesome!\",\"text\":\"Congrats for sending test email with Mailtrap!\",\"category\":\"Integration Test\"}"
headers = {
  "Authorization": "Bearer ",
  "Content-Type": "application/json"
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)