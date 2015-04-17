import smtplib
import sys

__author__ = 'Denis'
import SocketServer
import logging


def start_server():
    HOST, PORT = "127.0.0.1", int(sys.argv[2])

    server = SocketServer.TCPServer((HOST, PORT), SMTPServer, False)
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    return server

class SMTPServer(SocketServer.BaseRequestHandler):
    server_name = sys.argv[1]
    mail_dir = 'C:/mail'
    server_addr = {'another': 'localhost'}
    server_ports = {'another': 2526}

    def fetch_command(self):
        buffer = ""
        while "\r\n" not in buffer:
            new_data = self.request.recv(1024)
            buffer += new_data
        print("<< " + buffer)
        return buffer.partition("\r\n")[0]

    def send_response(self, code, message):
        response = str(code) + ' ' + message + '\r\n'
        print(">> " + response)
        self.request.send(response)

    def store_msg(self, msg, user):
        f = open(self.mail_dir + '/' + user, 'a')
        f.write("From MAILER-DAEMON\r\n")
        f.write(msg + "\r\n")
        f.close()

    def forward_msg(self, msg, addr, domain):
        if domain not in self.server_ports:
            print("Unknown server!")
            return
        server = smtplib.SMTP(self.server_addr[domain], self.server_ports[domain])
        server.set_debuglevel(1)
        server.sendmail(self.from_addr, addr, msg)
        server.quit()

    def route_mail(self, msg):
        for addr in self.to:
            user, sep, domain = addr.partition('@')
            if domain == self.server_name:
                self.store_msg(msg, user)
            else:
                self.forward_msg(msg, addr, domain)

    def handle(self):
        self.send_response(220, 'Hello')

        self.from_addr = ""
        self.to = []

        while True:
            command = self.fetch_command()
            cmd_up = command.upper()
            if cmd_up.startswith('HELO'):
                self.send_response(250, 'DenisServer')
            elif cmd_up.startswith('AUTH LOGIN'):
                self.send_response(334, 'VXNlcm5hbWU6')
                self.fetch_command()
                self.send_response(334, 'UGFzc3dvcmQ6')
                self.fetch_command()
                self.send_response(235, '2.7.0 Authentication successful.')
            elif cmd_up.startswith('MAIL FROM'):
                self.from_addr = command.partition('<')[2].partition('>')[0]
                self.send_response(250, 'OK')
            elif cmd_up.startswith('RCPT TO:'):
                address = command.partition('<')[2].partition('>')[0]
                self.to.append(address)
                self.send_response(250, "OK")
            elif cmd_up == 'DATA':
                self.send_response(354, 'Enter mail, end with "." on a line by itself')
                data = ""
                while "\r\n.\r\n" not in data:
                    data += self.request.recv(1024)
                    print(data)
                msg = data.rpartition(".\r\n")[0]
                self.route_mail(msg)
                self.send_response(250, "OK")
            elif cmd_up == 'QUIT':
                self.send_response(221, "Quit OK")
                self.request.close()
                return
            else:
                self.send_response(502, "DenisServer Wrong Command!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = start_server()
    server.serve_forever()