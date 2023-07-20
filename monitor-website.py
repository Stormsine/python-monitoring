import paramiko as paramiko
import requests
import smtplib
import os

import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def restart_container():
    def restart_server_and_container():
        # restart linode server
        print('Rebooting the server...')
        client = linode_api4.LinodeClient(LINODE_TOKEN)
        nginx_server = client.load(linode_api4.Instance, )
        nginx_server.reboot

        while True:
            nginx_server = client.load(linode_api4.Instance, )
            if nginx_server.status == 'running':
                time.sleep(5)
                restart_container()
                break


response = requests.get('http://li1388-236.members.linode.com:8080/')
if response.status_code == 200:
    print('Application is running successfully!')
else:
    print('Application Down. Fix it!')
    # send email to me
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = "Subject: Site Down\nFix the issue! Restart the application"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='', username='root', key_filename='/users/mrsam/.ssh/id_rsa')
        stdin, stdout, stderr = ssh.exec_command('docker start')
        print(stdout.readlines())
        ssh.close()

schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run_pending()
