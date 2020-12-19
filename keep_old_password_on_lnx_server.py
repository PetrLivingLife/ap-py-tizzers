from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import AuthenticationException
from time import sleep


class ChangeExpiredPassword(object):
    def __init__(self, server, username, password):
        # self.ssh = SSHClient()
        # self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.username = username
        self.password = password
        self.temp_password = "DocasneHesloTralala2018*03"
        self.server = server
        self.password_required_text = "You must change your password now and login again"
        self.new_password_text = "New password:"
        self.retype_password_text = "Retype new password:"
        self.change_success = "all authentication tokens updated successfully"
        self.passwd_change_text = "Changing password for"
        self.no_success = "    #### No success. Check and change manually. {} ####"
        self.no_change_needed = "    #### No need to change passwords. ####"

        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())

        self.term = None
        self.connect_shell(server=self.server, username=self.username, password=self.password)

        if self.term:

            if self.password_required_text in self.decode_output(self.get_term_output(self.term)):
                if self.set_temp_password(self.term, self.password, self.temp_password):
                    if self.term.closed:
                        self.connect_shell(server=self.server, username=self.username, password=self.temp_password)
                        self.set_old_password_back(self.term, self.password, self.temp_password)
            else:
                print(self.no_change_needed)

            self.term.close()
            self.ssh.close()

    def set_temp_password(self, term, old, temp):
        term.send(old + "\n")
        if self.new_password_text in self.decode_output(self.get_term_output(term)):
            term.send(temp+"\n")
            if self.retype_password_text in self.decode_output(self.get_term_output(term)):
                term.send(temp+"\n")
                if self.change_success in self.decode_output(self.get_term_output(term)):
                    print("    #### Password changed to temporary: {}. ####".format(temp))
                    return True

        print(self.no_success.format("Temporary password not set."))
        return False

    def set_old_password_back(self, term, old, temp):
        term.send("passwd\n")
        if self.passwd_change_text in self.decode_output(self.get_term_output(term)):
            term.send(temp + "\n")
            if self.new_password_text in self.decode_output(self.get_term_output(term)):
                term.send(old + "\n")
                if self.retype_password_text in self.decode_output(self.get_term_output(term)):
                    term.send(old + "\n")
                if self.change_success in self.decode_output(self.get_term_output(term)):
                    print("    #### Password changed back to old: {}. ####".format(old))
                    return True

        print(self.no_success.format("Old password not set."))
        return False

    def get_term_output(self, term):
        buff = b''
        while True:
            buff += term.recv(9999)
            # print(buff)
            sleep(0.5)
            if not term.recv_ready():
                break

        return buff

    def decode_output(self, response):
        resp = response.decode("utf8")
        # print(resp)
        return resp

    def connect_shell(self, server, username, password):
        try:
            self.ssh.connect(hostname=server, username=username, password=password)
            self.term = self.ssh.invoke_shell()
        except AuthenticationException:
            print("    #### Wrong login/password: %s, %s, %s." % (server, username, password))


class Run(object):
    def __init__(self):
        with open(r"./servers.txt") as f:
            self.servers = [tuple(line.strip().split(',')) for line in f.readlines()]

            for server, username, password in self.servers:
                print("Changing password on : %s" % server)
                ChangeExpiredPassword(server=server, username=username, password=password)


if __name__ == '__main__':
    Run()
