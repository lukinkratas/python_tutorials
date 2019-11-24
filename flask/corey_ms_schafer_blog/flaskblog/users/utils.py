from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message
import os
import secrets
from PIL import Image


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static', 'profile_pics', picture_fn)

    output_size = (500, 500)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request',
                sender='noreply@blog.com',
                recipients=[user.email])
    msg.body = 'To reset your password, visit following link:\n'
    msg.body += f'{url_for("users.reset_token", token=token, _external=True)} \n'
    msg.body += '\n'
    msg.body += 'If you did not make this request, ignore the email and no changes will be made.'

    mail.send(msg)