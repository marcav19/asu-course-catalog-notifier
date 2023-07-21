# my-first-bot
When running, every fifteen minutes the bot will make an HTTP GET request to the ASU course catalog API and extracts seating data from the returned JSON object.
If there is a seat open, an email is sent to me alerting me of the opening.

This project utilizes the Microsoft Outlook SMTP servers to send the email to myself.
