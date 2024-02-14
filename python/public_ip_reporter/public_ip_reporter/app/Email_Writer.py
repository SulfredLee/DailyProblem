from sfdevtoolslight.devTools.Email_Helper import *

class Email_Writer(Email_Helper):
    def __init__(self):
        pass

    def Send_Email(self
                   , attachments: List[Path]
                   , sender_email: str
                   , sender_pw: str
                   , receiver_emails: List[str]) -> None:
        '''
        Send email with attachments
        '''
        current_time: str = datetime.now().strftime("%Y%m%d_%H%M%S")

        message = MIMEMultipart("alternative")
        message["Subject"] = f"(PRD)(Report) {current_time} public ip"
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

        self.__Send_Email_Outlook(message=message
                                  , sender_email=sender_email
                                  , sender_pw=sender_pw
                                  , receiver_emails=receiver_emails)

        return None

    def __Send_Email_Outlook(self
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
