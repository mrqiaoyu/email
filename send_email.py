from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib


class SendEmail:
    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send(self, addr_from, addr_to, password, server, port, title_from='', title_to='', title_head='', text='', html=''):
        msg = MIMEMultipart('alternative')
        msg['From'] = self._format_addr(title_from + '<%s>' % addr_from)
        msg['To'] = self._format_addr(title_to + '<%s>' % addr_to)
        msg['Subject'] = Header(title_head, 'utf-8').encode()
        msg.attach(MIMEText(text, 'plain', 'utf-8'))
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        try:
            server = smtplib.SMTP_SSL(server, port)
            server.set_debuglevel(1)
            server.login(addr_from, password)
            server.sendmail(addr_from, addr_to, msg.as_string())
            server.quit()
        except smtplib.SMTPException as e:
            print('发送邮件出错：', e)
