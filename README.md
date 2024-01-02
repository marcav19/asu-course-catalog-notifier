# ASU Course Catalog Notifier
Every fifteen minutes, this project will make an HTTP GET request to the ASU course catalog API which returns a JSON object. Then the JSON object is manipulated to extract relevant course seating availability information.
If there is a seat open, an email is sent to me notifying me of the new availability.

This project utilizes the Microsoft Outlook SMTP servers to send an email notification.
