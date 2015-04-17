__author__ = 'Denis'

import socket, base64, ssl, getpass
import ssl
HAVE_SSL = True


class POP3Client:

    def __init__(self,servers,ports):
        self.sock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ssl_version=ssl.PROTOCOL_SSLv23)
        self.server = servers
        self.port = ports

    def send(self, str):
        print(">> " + str)
        self.sock.send(str)

    def recv(self):
        self.answer = self.sock.recv(1024)
        print("<< " + self.answer)

    def recv2(self):
        self.answer = ""
        while not '.' in self.answer.splitlines():
            new_data = self.sock.recv(1024)
            self.answer += new_data
        print("<< " + self.answer)

    def command(self, cmd, wait_dot=False):
        self.send(cmd+"\n")
        if wait_dot:
            self.recv2()
        else:
            self.recv()
        assert self.answer.startswith("+OK")
        return self.answer


    def connect_to_serv(self):
        self.sock.connect((self.server,self.port))
        self.recv()
        self.command("USER denispopclient1994@yandex.ru")
        self.command("PASS denis11021994")
        """print("Input username")
        username = raw_input()
        self.command("USER "+username)
        print ("Input password")
        password = raw_input()
        self.command("PASS "+password)"""


    def stat(self):
        """cmd = self.command('STAT')
        parse = cmd.split(' ')
        num = int(parse[1])
        size = int(parse[2])
        return num"""
        return self.command('STAT')

    def list(self, which=None):
        return str(self.command('LIST %s' % which))

    def top(self, which, howmuch):
        return self.command('TOP %s %s' % (which, howmuch),True)

    def uidl(self, which=None):
        return self.command('UIDL %s' % which)

    def retr(self, which):
        return self.command('RETR %s' % which,True)

    def dele(self, which):
        return self.command('DELE %s' % which)

    def rset(self):
        return self.command('RSET')


    def quit(self):
        return self.command('QUIT')
        self.sock.close()

    def par_list(self,num=None):
        if num == None:
            print("Input num")
            num=raw_input()
        self.list(num)

    def par_top(self,msg=None,num=None):
        if msg == None:
            print("Input number of msg")
            msg=raw_input()
        if num == None:
            print("Input number of strings")
            num=raw_input()
        self.top(int(msg),int(num))

    def par_uidl(self,msg=None):
        if msg == None:
            print("Input number of msg")
            msg=raw_input()
        self.uidl(msg)

    def par_retr(self,msg=None):
        if msg == None:
            print("Input number of msg")
            msg=raw_input()
        self.retr(msg)

    def par_dele(self,msg=None):
        if msg == None:
            print("Input number of msg")
            msg=raw_input()
        self.dele(int(msg))

    """def control(self,msg):
        parse = cmd.split(' ')
        num = int(parse[1])
        size = int(parse[2])
        return num
        if (msg>self.connect_to_serv()):
            print ("Such number of the letter doesn't exist")
            return False
        else:
            return  True"""

def main():
    """print("Input name of server")
    server=raw_input()
    print("Input port")
    port=raw_input()
    client = POP3Client(server, int(port))"""
    client = POP3Client('pop.yandex.ru', 995)
    client.connect_to_serv()
    commands = {
        'stat': client.stat,
        'list': client.par_list,
        'top': client.par_top,
        'retr': client.par_retr,
        'uidl': client.par_uidl,
        'dele': client.par_dele,
        'rset': client.rset,
        'quit':  client.quit,

        }
    cmd=''
    while cmd != 'quit':
        print("Input command")
        cmd = raw_input()
        parse=cmd.split(' ')
        if parse[0] in commands:
            command = commands[parse[0]]
            command(*parse[1:])
        else:
            print("Wrong command")
        # if cmd == 'STAT':
        #     client.stat()
        # elif parse[0] == 'TOP':
        #     if len(parse)==1:
        #         client.print_top()
        #     elif len(parse)==2:
        #         client.print_top(parse[1])
        #     else:
        #         client.print_top(parse[1],parse[2])
        # elif parse[0] == 'LIST':
        #     if len(parse)==1:
        #         client.print_list()
        #     else:
        #         client.print_list(parse[1])
        # elif parse[0] == 'UIDL':
        #     if len(parse)==1:
        #         client.print_uidl()
        #     else:
        #         client.print_uidl(parse[1])

    #denispopclient1994@yandex.ru
    #denis11021994
if __name__ == "__main__":
   main()
