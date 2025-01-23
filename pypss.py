import sys
import time
try:
    import paramiko
except Exception:
    print("Libs not found!")
    sys.exit()


class ssh_connect:
    def __init__(self,ip,commands=[]):
        self.ip = ip
        self.commands = commands
        self.cmdres = {}
        self.uname = "cli"
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect()
        self.genCmdinit()
        self.terminator()


    def wait(self,keyword):
        output=""
        while True:
            output += self.ch.recv(1).decode()
            if keyword in output:
                break
        return output

    def connect(self):
        try:
            self.ssh.connect(self.ip,22,self.uname,"")
            time.sleep(0.25)
            self.ch = self.ssh.invoke_shell()            
            time.sleep(0.25)
            self.ch.sendall(f"admin\n")
            self.wait("Password:")
            time.sleep(0.25)
            self.ch.sendall(f"admin\n")
            self.wait("(Y/N)?")
            time.sleep(0.25)
            self.ch.sendall("y\n")
            self.wait("#")
            time.sleep(0.25)

        except paramiko.AuthenticationException:
            print("Communication/Login failure! Press Enter to exit...")
            sys.exit()

    def genCmdinit(self):
        time.sleep(1)
        for c in self.commands:
            self.initiator(c)
            time.sleep(0.5)

    def initiator(self,cmd):
        self.ch.sendall('{0}\n'.format(cmd))
        if "logout" in cmd:
            return
        else:
            self.cmdres[cmd] = self.wait("#")

    def terminator(self):
        self.ssh.close()
        print("Closing ssh session.")



if __name__ == "__main__":
    x = ssh_connect("100.124.197.216",["show version","show xc brie","show slot *"])
    print(x.cmdres["show version"])
    print(x.cmdres["show xc brie"])
    print(x.cmdres["show slot *"])
