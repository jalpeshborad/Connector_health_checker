# coding: utf-8
# -*- coding: utf-8 -*-

__author__ = "Jalpesh Borad"
__copyright__ = "Copyright 2018"

__version__ = "0.0.1"
__maintainer__ = "Jalpesh Borad"
__email__ = "jalpeshborad@gmail.com"
__status__ = "Development"

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, message):
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(from_add, PASSWORD)

    msg = MIMEMultipart()
    msg['From'] = from_add
    msg['To'] = to_add
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))
    s.sendmail(from_add, to_add, msg.as_string())
    del msg
    s.quit()
