from django.core.mail import send_mail


def send_notification_email(
        original_comment_author_email, reply_author, reply_text
):
    """Function to send email notification when someone replies to your comment"""

    subject = f"New Reply from {reply_author}"
    message = f"Hello,\n\n{reply_author} has replied to your article. Reply: {reply_text}.\n"
    from_email = "nazarivankiv1@gmail.com"
    recipient_list = [original_comment_author_email]
    send_mail(subject, message, from_email, recipient_list)
