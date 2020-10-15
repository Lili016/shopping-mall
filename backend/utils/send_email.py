from threading import Thread

from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    dict(
        DEBUG=False,
        MAIL_SERVER="smtp.163.com",
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_PASSWORD='PBPKKJRVSGLDXAUX',
        MAIL_USERNAME="lee19980106@163.com",
    )
)

mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, base_url, token):
    msg = Message(subject, sender='lee19980106@163.com', recipients=[to])
    verify_url = base_url + "?token=" + token
    msg.html = (
        "<p>尊敬的用户您好！</p>"
        "<p>感谢您使用美多商城。</p>"
        "<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>"
        '<p><a href="%s">%s<a></p>' % (to, verify_url, verify_url)
    )

    # 通过线程发送信息      tr = Thread(target=send_async_email, args=[app, msg])
    tr = Thread(target=send_async_email, args=[app, msg])
    tr.start()
    return tr
