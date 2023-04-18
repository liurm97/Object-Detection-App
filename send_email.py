import smtplib
from email.message import EmailMessage
import os
import imghdr

PASSWORD = os.getenv("PASSWORD")
SENDER = "app1sendemail@gmail.com"
RECIPIENT = "fellowe5@hotmail.com"
CONTEXT = "smtp.gmail.com"
def emailing(image_to_send):
    email_message = EmailMessage()
    email_message['Subject'] = "You have captured something on image"
    email_message.set_content("Hey something was caught in the video!")

    with open(image_to_send, "rb") as f:
        content = f.read()

    # Add email attachment
    # imghdr.what() returns type of image. In this case - "png"
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP(CONTEXT, port=587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECIPIENT, msg=email_message.as_string())
    gmail.quit()

if __name__ == "__main__":
    emailing("images/Screenshot_1.png")