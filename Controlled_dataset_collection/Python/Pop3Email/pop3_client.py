import telnetlib
import sys
import time

if __name__ == "__main__":
    number_of_emails_to_send = int(sys.argv[1])
    number_of_emails_to_send *= 30  # to make a 75 KB email
    email_server_ip = '10.0.1.5'
    email_server_port = 10111

    temp_number_of_emails_to_send = number_of_emails_to_send if number_of_emails_to_send < 3000 else 3000
    number_of_emails_to_send -= temp_number_of_emails_to_send
    tn = telnetlib.Telnet(email_server_ip, email_server_port)
    tn.read_until(b"+OK pypopper file-based pop3 server ready")
    data_to_send = str(number_of_emails_to_send) + ':0'
    tn.write(data_to_send.encode("ascii") + b"\n")
    print(tn.read_all())
    tn.close()

    while number_of_emails_to_send > 0:
        time.sleep(1)
        temp_number_of_emails_to_send = number_of_emails_to_send if number_of_emails_to_send < 300 else 300
        number_of_emails_to_send -= temp_number_of_emails_to_send
        tn = telnetlib.Telnet(email_server_ip, email_server_port)
        tn.read_until(b"+OK pypopper file-based pop3 server ready")
        data_to_send = str(number_of_emails_to_send) + ':0'
        tn.write(data_to_send.encode("ascii") + b"\n")
        print(tn.read_all())
        tn.close()


