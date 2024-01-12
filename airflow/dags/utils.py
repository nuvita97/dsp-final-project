import smtplib
from email.mime.text import MIMEText
import logging
import psycopg2


def send_email_notification(sender, recipients, subject, message):
    # Create the message
    message = MIMEText(message)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipients
    # message["To"] = ", ".join(recipients)

    # Establish a connection with the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("vietthai230397@gmail.com", "jrtt yohf xrig dcxi")
        server.sendmail(sender, recipients, message.as_string())


def alert_user_by_email(df):
    sender = "vietthai230397@gmail.com"
    recipients = "viet-thai.nguyen@epita.fr"
    # recipients = ["viet-thai.nguyen@epita.fr",
                #   "stephanie-lynn-rule.arthaud@epita.fr"]
    subject = "Alert: New Data Quality Issues !"
    message = f"{len(df)} issues detected. Check the logs for details."
    logging.info(message)

    send_email_notification(sender, recipients, subject, message)


def write_logs_to_db(index, row):
    # Get the values from row df
    file_name = row['file_name']
    review_text = row['reviewText']
    problem = row['validated']

    # Write problematic logs to Postgres
    conn = psycopg2.connect("host=host.docker.internal port=5432 dbname=amazon-reviews user=postgres password=password")
    cur = conn.cursor()
    sql = """INSERT INTO problem (file_name, review_text, problem, time)
            VALUES(%s, %s, %s, now()) RETURNING id;"""
    cur.execute(sql, (file_name, review_text, problem))
    cur.fetchone()[0]
    conn.commit()     
    cur.close()    