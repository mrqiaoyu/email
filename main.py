import configparser
import re
import json
import getpass
from send_email import SendEmail as se

class EmailService:
    def __init__(self):
        self.user = self.get_user_info()
        self.email_config = self.get_mail_info()

    def get_user_info(self):
        user = {}
        config = configparser.ConfigParser()
        try:
            config.read('config/user.conf')
            user['email'] = config.get('user', 'email')
            user['password'] = config.get('user', 'password')
        except:
            print('获取邮箱密码出错，请手动输入~')
            user['email'] = input("请输入邮箱：")
            user['password'] = getpass.getpass("请输入密码：")
        return user

    def get_mail_info(self):
        info = {}
        try:
            with open('config/email.json', 'r', encoding='utf-8') as f:
                info = json.load(f)
                return info
        except Exception as e:
            print("读取 email 配置文件出错：", e)
            return

    def main(self):
        server = se()

        if self.email_config is None:
            return

        message = self.email_config['message']
        for e in self.email_config['email']:
            if 'message' in e:
                message = e['message']
            server.send(self.user['email'], e['email'], self.user['password'], self.email_config['server'], self.email_config['port'],  message['title_from'], message['title_to'], message['title_head'], message['text'], message['html'])


if __name__ == '__main__':
    email = EmailService()
    email.main()
