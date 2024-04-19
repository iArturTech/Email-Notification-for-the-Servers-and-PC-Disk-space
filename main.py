import psutil
import smtplib
from email.mime.text import MIMEText
import logging
import datetime

# Email AH
smtp_server = "inputhere"
smtp_port = inputport
username = "inputhere@email.com"
password = "inputhere"
from_email = "inputhereSenderEmailAdd"
to_email = "inputhereReceiverEmailAdd"

# drives to check AH
drives = ["\\\PC06-w6\\c$", "\\\srv16\\c$", "\\\srv16\\d$"]

# Configure logging
logging.basicConfig(filename='drive_check.log', level=logging.INFO)

# start time AH
start_time = datetime.datetime.now()
logging.info("Script started at {}".format(start_time))

# Check drive space AH
for drive in drives:
    try:
        usage = psutil.disk_usage(drive)
        if usage.free < 5 * (1024 ** 3):
            # Send email notification
            subject = "Low Disk Space Alert: {}".format(drive)
            message = "Drive {} has only {:.2f} GB free space remaining.".format(drive, usage.free / (1024 ** 3))
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = to_email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
                logging.info("Email sent for drive: {}".format(drive))
        else:
            logging.info("Drive {} has more than 5 GB free space, skipping email.".format(drive))
    except PermissionError as e:
        logging.error("PermissionError occured while checking drive {}: {}".format(drive, e))
    except FileNotFoundError as e:
        logging.error("FileNotFoundError occured while checking drive {}: {}".format(drive, e))
    except Exception as e:
        logging.error("Error occured while checking drive {}: {}".format(drive, e))

# Log end time AH
end_time = datetime.datetime.now()
logging.info("Script ended at {}".format(end_time))
