import yaml
import getpass
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from datetime import datetime
import smtplib
from email.message import EmailMessage

def read_devices(file_path):
    with open(file_path) as f:
        return yaml.safe_load(f)

def read_commands(file_path):
    with open(file_path) as f:
        return [cmd.strip() for cmd in f.readlines() if cmd.strip()]

def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'sudarshan991212@gmail.com'
    msg['To'] = to_email

    # Gmail SMTP setup
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('sudarshan991212@gmail.com', 'pygrffnoergscrfn')  # your 16-digit app password, no spaces
        smtp.send_message(msg)

def main():
    devices = read_devices('devices.yaml')
    commands = read_commands('commands.txt')

    combined_output = ""
    for device in devices:
        print(f"\nConnecting to {device['host']}...")
        password = getpass.getpass(f"Enter password for {device['host']}: ")
        device['password'] = password
        try:
            connection = ConnectHandler(**device)
            output = f"\nOutput for device {device['host']}:\n"
            for cmd in commands:
                cmd_output = connection.send_command(cmd)
                output += f"\n--- Command: {cmd} ---\n{cmd_output}\n"
            connection.disconnect()
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
            output = f"\nOutput for device {device['host']}:\n\nError: {str(e)}\n"
        print(output)
        combined_output += output

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"output_log_{timestamp}.txt", "w") as f:
        f.write(combined_output)

    # Change this to your own email where you want the report
    send_email("Netmiko Automation Report", combined_output, "sudarshan991212@gmail.com")

if __name__ == "__main__":
    main()