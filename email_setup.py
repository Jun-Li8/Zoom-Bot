import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import json

#TODO: Finalize the user data to be sent in the email.
#data is a dictionary
def sent_email():
    today = datetime.now()
    date = today.strftime("%m/%d/%Y %H:%M:%S")
    message = MIMEMultipart()
    message["Subject"] = "Summary of Your Meeting"
    message["From"] = "zoombullies338@gmail.com" #create your own email to send
    message["To"] = 'convoztesting@gmail.com' #email that you are sending to
    #Adjust html to how you want it to look like
    html = """\
    <html>
        <head>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <h1 style="text-align: center">Today's Meeting</h1>
            <hr>
            <h2 style ="text-align: left;">Meeting </span> on
            <span style="color:#A53FD2; font-weight: normal">{1}</span></h2>
            <h2 style="text-align: left;"> Attendees: <span style="color:black; font-weight: normal">{2}</span></h2>
            <hr>
            <h2 style ="color:#659EC7; text-align: left"> Number of Bullying Detections: <span style="color:black; font-weight: normal"> 5 </span> </h2>
            <hr>
            <h2 style ="color:#659EC7; text-align: left">Types of Bullying: </h2>
                <h2 style ="color:black; text-align: left; padding-left: 40px; font-weight: normal"> Personal Attacks </h2>
                <h2 style ="color:black; text-align: left; padding-left: 40px; font-weight: normal"> Sexual Advances </h2>
            <hr>
            <br>
            <form action="http://localhost:8000/">
                <input style="background-color: #659EC7; display: block; outline: none; border: none;width: 300px; height: 70px;border-radius: 30px;color: white;font-size: 1.5rem;font-weight: 600;color: var(--text);background-size: 100% 100%;margin-bottom: 15px;box-shadow: 0 0 0 7px var(--light) inset;position: absolute;left: 50%;" type="submit" value="View more details" />
            </form>
        </body>
    </html>
    """.format('Jun', date, 'Jun, Xin, Jae, Shalom, Terry')

    part = MIMEText(html, "html")

    message.attach(part)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("zoombullies338@gmail.com", "compsci21")
        server.sendmail(
            "zoombullies338@gmail.com", 'convoztesting@gmail.com', message.as_string()
        )
sent_email()