from django.core.mail import send_mail

def sendMail(subject, message, recipient_list, isHtml):
    try:
        print("### Sending Email #######")
        if isHtml:
            send_mail(subject=subject,
                message="",
                from_email='support@invelps.com',
                recipient_list=recipient_list,
                fail_silently=False,
                html_message=message
                )
        else:
            send_mail(subject=subject,
                from_email='support@invelps.com',
                recipient_list=recipient_list,
                fail_silently=False,
                message=message
                )
    except Exception as ex:
        print(ex)


# import smtplib, ssl
# from email.mime.text import MIMEText

# def sendMail(subject, message, to_mail):
#     host = 'smtp.hostinger.com'
#     port = 465
#     msg = MIMEText(message)
#     msg['Subject'] = subject
#     msg['From'] = 'support@invelps.com'
#     msg['To'] = to_mail[0]
#     print("##### CREATING SSL CONTEXT ######")
#     try: 
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL(host, port, context=context) as server:
#             # server.starttls()
#             print("##### ATTEMPTING TO LOGIN TO SMTP SERVER ######")
#             server.login('support@invelps.com', 'Support1nvelps@zmlk')
#             print("##### ATTEMPTING TO SEND AN EMAIL FROM SMTP SERVER ######")
#             server.sendmail('support@invelps.com', to_mail, msg.as_string())
#             print("##### SENT EMAIL FROM SMTP SUCCESSFULLY #####")
#     except Exception as ex:
#         print("##### SMTP EXCEPTION OCCURED #####")
#         print(ex)
    