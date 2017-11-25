#!/usr/bin/env python
# encoding:utf-8 
import requests

def send_message(to_email, to_subject, to_content):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox0c70477293904d38a6c42c8dd571502f.mailgun.org/messages",
        auth=("api", "key-30d66261eb01af03240b479fabde0794"),
        data={"from": "mq<mq@sandbox0c70477293904d38a6c42c8dd571502f.mailgun.org>",
              "to": to_email,
              "subject": to_subject,
              "text": to_content})


if __name__ == '__main__':
    # example
    result = send_message(["27130723@qq.com"], "douban-links", "cccccccc")
    if result.status_code == 200:
        print "邮件发送成功"
    else:
        print "邮件发送失败"