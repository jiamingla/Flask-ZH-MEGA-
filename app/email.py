from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    #print(msg)
    Thread(target=send_async_email, 
            args=(current_app._get_current_object(), msg)).start()
    #current_app._get_current_object()表示式從代理物件中提取實際的應用例項，
    # 所以它就是我作為引數傳遞給執行緒的。
"""
#這個函式中有趣的部分是電子郵件的文字和 HTML 內容
# 是使用熟悉的render_template()函式從模板生成的。 
# 模板接收使用者和令牌作為引數，以便可以生成個性化的電子郵件訊息。 
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[Microblog] Reset Your Password'),
    sender=app.config['ADMINS'][0],
    recipients=[user.email],
    text_body=render_template('email/reset_password.txt', user=user, token=token),
    html_body=render_template('email/reset_password.html', user=user, token=token))
"""
