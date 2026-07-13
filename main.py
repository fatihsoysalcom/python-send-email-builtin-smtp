import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header # For proper handling of non-ASCII characters in headers

def send_email_without_libraries():
    """
    Sends a simple text email using Python's built-in smtplib and email modules.
    Configuration is read from environment variables.
    """
    # --- Configuration from Environment Variables ---
    # Set these environment variables before running the script.
    # For Gmail, you might need to generate an "App password" if 2FA is enabled.
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    
    # Default to common Gmail SMTP settings if not specified
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587')) # 587 for TLS, 465 for SSL

    if not all([sender_email, sender_password, receiver_email]):
        print("Error: Please set SENDER_EMAIL, SENDER_PASSWORD, and RECEIVER_EMAIL environment variables.")
        print("Example: export SENDER_EMAIL='your_email@example.com'")
        print("         export SENDER_PASSWORD='your_app_password'")
        print("         export RECEIVER_EMAIL='recipient@example.com'")
        return

    # --- Create the Email Message ---
    # The 'email' package (part of Python's standard library) is used to construct the message.
    # MIMEText is used for plain text emails.
    email_body = "This is a test email sent from Python without any external libraries.\n\n" \
                 "This demonstrates the power of Python's built-in smtplib and email modules."
    msg = MIMEText(email_body, 'plain', 'utf-8')

    # Set email headers. Using Header for subject ensures proper encoding for non-ASCII characters.
    msg['Subject'] = Header('Python Built-in Email Test', 'utf-8')
    msg['From'] = sender_email
    msg['To'] = receiver_email

    print(f"Attempting to send email from {sender_email} to {receiver_email} via {smtp_server}:{smtp_port}...")

    # --- Send the Email using smtplib ---
    try:
        # smtplib.SMTP is used for connecting to an SMTP server.
        # For port 587 (TLS), we connect and then call starttls().
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo() # Can be omitted, but good practice to identify yourself to the SMTP server
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.ehlo() # Call ehlo() again after starttls()
            
            # Login to the SMTP server with your credentials
            server.login(sender_email, sender_password)
            
            # Send the email. msg.as_string() converts the MIMEText object to a string.
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("\nError: SMTP Authentication Failed.")
        print("Please check your SENDER_EMAIL and SENDER_PASSWORD.")
        print("If using Gmail, ensure you've generated an 'App password' and use that instead of your regular password.")
        print("Also, ensure 'Less secure app access' is OFF in your Google account settings.")
    except smtplib.SMTPConnectError as e:
        print(f"\nError: Could not connect to SMTP server: {e}")
        print("Please check your SMTP_SERVER and SMTP_PORT environment variables.")
        print("Ensure the server address and port are correct and accessible.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    send_email_without_libraries()
