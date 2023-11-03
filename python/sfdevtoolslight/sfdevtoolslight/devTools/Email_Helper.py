from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Dict, List, Set, Tuple, Union, Any
from pathlib import Path
from bs4 import BeautifulSoup, Tag
from datetime import datetime
import smtplib, ssl

class Email_Helper(object):
    def __init__(self):
        pass

    def Send_Test_Email(self, sender_email: str, sender_pw: str, receiver_email: str) -> None:
        message = MIMEMultipart("alternative")
        message["Subject"] = "(UAT) Test email"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """\
        Hi,
        How are you?
        Do you want some juice?
        """
        html = """\
        <html>
          <body>
            <p>Hi,<br>
               How are you?<br>
               <a href="https://www.youtube.com/watch?v=VnvfBWusrPk">Do you want some juice?</a>
            </p>
          </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        self.Send_Email(message=message
                        , sender_email=sender_email
                        , sender_pw=sender_pw
                        , receiver_emails=[receiver_email])


        return None

    def Send_Test_002(self
                      , attachments: List[Path]
                      , sender_email: str
                      , sender_pw: str
                      , receiver_emails: List[str]) -> None:
        '''
        This is a test case with attachments
        '''
        current_time: str = datetime.now().strftime("%Y%m%d_%H%M%S")

        message = MIMEMultipart("alternative")
        message["Subject"] = f"(PRD)(Report) {current_time} test report"
        message["From"] = sender_email
        message["To"] = ",".join(receiver_emails)

        # handle email content
        soup = BeautifulSoup()
        html = Tag(builder=soup.builder, name="html")
        pa = Tag(builder=soup.builder, name="p")
        soup.append(html)
        html.append(pa)
        pa.append("Please find your reports in the attachments.")
        message.attach(MIMEText(soup.prettify(), "html"))

        # handle attachment
        for attachment in attachments:
            with open(attachment, "rb") as fh:
                part = MIMEApplication(fh.read(), Name=attachment.name)

                part["Content-Disposition"] = f'attachment; "filename={attachment.name}"'
                message.attach(part)

        self.Send_Email(message=message
                        , sender_email=sender_email
                        , sender_pw=sender_pw
                        , receiver_emails=receiver_emails)

        return None


    def __Send_Email(self
                     , message: MIMEMultipart
                     , sender_email: str
                     , sender_pw: str
                     , receiver_emails: List[str]) -> None:
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_pw)
            server.sendmail(
                sender_email, receiver_emails, message.as_string()
                )

        return None
