#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
import mechanize, re, threading, os, commands, random
from sys import argv
import readline



###############supposedly complete the path and commands###################
COMMANDS = ['title', 'paste', 'exposure', 'expiration',
            'syntax', 'foobar', 'foo']
RE_SPACE = re.compile('.*\s+$', re.M)

class Completer(object):

    def _listdir(self, root):
        "List directory 'root' appending the path separator to subdirs."
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
            res.append(name)
        return res

    def _complete_path(self, path=None):
        "Perform completion of filesystem path."
        if not path:
            return self._listdir('.')
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p)
                for p in self._listdir(tmp) if p.startswith(rest)]
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._listdir(path)]
        # exact file match terminates this completion
        return [path + '']

    def complete_extra(self, args):
        "Completions for the 'extra' command."
        if not args:
            return self._complete_path('.')
        # treat the last arg as a path and complete it
        return self._complete_path(args[-1])

    def complete(self, text, state):
        "Generic readline completion entry point."
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        # show all commands
        if not line:
            return [c + ' ' for c in COMMANDS][state]
        # account for last argument ending in a space
        if RE_SPACE.match(buffer):
            line.append('')
        # resolve command to the implementation function
        cmd = line[0].strip()
        impl = getattr(self, 'complete_%s' % "extra")
        args = line[0:]
        if args:
            return (impl(args) + [None])[state]
        return [cmd + ''][state]
        results = [c + '' for c in COMMANDS if c.startswith(cmd)] + [None]
        return results[state]

comp = Completer()
# we want to treat '/' as part of a word, so override the delimiters
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab:complete")
readline.set_completer(comp.complete)
################################################################################






#generate a browser with user-agent
def genBrowser():

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_redirect(True)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    return br

always_safe = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
               'abcdefghijklmnopqrstuvwxyz'
               '0123456789' '_.-')
def quote(s, safe = '/'):   #quote('abc def') -> 'abc%20def'
        safe += always_safe
        safe_map = {}
        for i in range(256):
                c = chr(i)
                safe_map[c] = (c in safe) and c or  ('%%%02X' % i)
        res = map(safe_map.__getitem__, s)
        return ''.join(res)


#Begining of the class uploader
class unixhubuploader(threading.Thread):

    def __init__(self, title, paste, exposure, expiration, syntax):

        self.title      = title
        self.paste      = paste
        self.exposure   = exposure
        self.expiration = expiration
        self.syntax     = syntax
        self.br         = genBrowser()
        threading.Thread.__init__(self)




    #get what we need and place it into some variables
    def upload_from_file(self):

        try:
            self.paste = quote(self.paste)
            self.br._ua_handlers['_cookies'].cookiejar
            self.br.open("http://paste.unixhub.net/index.html")
            self.captcha = self.getcaptcha(self.br)
            self.br.open("http://paste.unixhub.net/index.html",
            "paste="+self.paste+"&syntax="+self.syntax+"&expiration="+self.expiration+"&exposure="+self.exposure+"&title="+self.title.replace(" ","+")+ "&txtCaptcha="+self.captcha+"&submit=Submit")
            #self.br.reload()
            #if "captcha" in self.br.response().read():
                #self.captcha = self.getcaptcha(self.br)
            #self.br.select_form(nr=1)
            #self.br.form['txtCaptcha']= self.captcha
            #self.br.form['title']     = self.title
            #self.br.form['exposure']  = [self.exposure]
            #self.br.form['expiration']= [self.expiration]
            #self.br.form['syntax']    = [self.syntax]
            #self.br.form['paste']     = self.paste
            #self.br.submit()

        except Exception, e:
            print e



    #handle the captcha stuff:
    def getcaptcha(self, br):

        img_response  = 'http://paste.unixhub.net/libs/captcha/create_image.php?'+str(random.uniform(0.0,1.0))
        img_response  = br.open_novisit(img_response)
        img           = img_response.read()
        writing       = open('unixhub.jpg','wb')
        writing.write(img)
        writing.close()
        threading.Thread(target=commands.getoutput, args=('feh "' + os.getcwd() + '"' + '/'+'unixhub.jpg',)).start()
        captcha       = raw_input(bcolors.OKBLUE+"\n["+bcolors.OKGREEN+"*"+bcolors.OKBLUE+"] "+bcolors.HEADER+"Please Enter the Captcha:\n"+bcolors.CYAN+"==> "+bcolors.OKGREEN)
        output        = [i for i in os.popen('ps -ef |grep %s' % 'feh') if not 'grep' in i]
        processID     = [i.split()[1] for i in output]
        for a in processID:
            os.kill(int(a), 9)
        return captcha

    #will one day handle the login process
    def login(self,username, passwd):

        #something will come here
        br.open("http://paste.unixhub.net/zone-login.html", "user="+username+"&pass"+passwd+"&button=Login")

    #RUN IT !!!
    def run(self):
        self.upload_from_file()
        print "\n"+bcolors.FAIL+self.br.geturl()
        os.system('rm unixhub.jpg')

#some stupid stuffs
exposures   = ["public",  "private"]
expirations = ["never", "1", "2", "3", "4"]
syntaxes    = ["c", "css", "cpp", "html4strict", "java", "perl", "php", "python", "ruby", "text", "asm", "xhtml", "actionscript", "ada", "apache", "applescript", "autoit", "bash", "bptzbasic", "c_mac", "csharp", "ColdFusion", "delphi", "eiffel", "fortran", "freebasic", "gml", "groovy", "inno", "java5", "javascript", "latex", "mirc", "mysql", "nsis", "objc", "ocaml", "oobas", "orcale8", "pascal", "plsql", "qbasic", "robots", "scheme", "sdlbasic", "smalltalk", "smarty", "sql", "tcl", "vbnet", "vb", "winbatch", "xml", "z80"]



#########COLORS#####################
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[1;32m'
    WARNING = '\033[93m'
    FAIL = '\033[0;31m'
    ENDC = '\033[0m'
    CYAN = '\033[1;36m'
    COOL = '\033[0;45m'
    COOL1 = '\033[1;45m'
    backgreen ='\033[1;44m'
##################################


def menu()
    os.system("./starter.sh")
    #some menu will go here
    title=""
    paste=""
    exposure=""
    expiration=""
    syntax=""

    while title=="" or title ==" ":
        title = raw_input(bcolors.OKBLUE+"\n["+bcolors.OKGREEN+"*"+bcolors.OKBLUE+"] "+bcolors.HEADER+"Enter a title for a paste:\n"+bcolors.CYAN+"==> "+bcolors.OKGREEN)
    while paste=="" or paste ==" ":
        try:
            paste = open(raw_input(bcolors.OKBLUE+"\n["+bcolors.OKGREEN+"*"+bcolors.OKBLUE+"] "+bcolors.HEADER+"Enter the File you want to paste:\n"+bcolors.CYAN+"==> "+bcolors.OKGREEN)).read()
        except:
            paste = ""
    while exposure not in exposures:
        exposure = raw_input(bcolors.OKBLUE+"\n["+bcolors.OKGREEN+"*"+bcolors.OKBLUE+"] "+bcolors.HEADER+"Do you want the paste to be public or private "+bcolors.OKBLUE+"["+bcolors.OKGREEN+"pub"+bcolors.OKBLUE+"/"+bcolors.OKGREEN+"priv"+bcolors.OKBLUE+"]"+bcolors.HEADER+":\n"+bcolors.CYAN+"==> "+bcolors.OKGREEN)
        if exposure =='pub':
            exposure = 'public'
        if exposure =='priv':
            exposure = 'private'
    while expiration not in expirations:
        expiration = raw_input(bcolors.OKBLUE+"\n["+bcolors.OKGREEN+"*"+bcolors.OKBLUE+"] "+bcolors.HEADER+"When do you want the paste to expire:\n"+bcolors.OKBLUE+"["+bcolors.OKGREEN+"1"+bcolors.OKBLUE+"]"+bcolors.HEADER+"10 Minutes\n"+bcolors.OKBLUE+"["+bcolors.OKGREEN+"2"+bcolors.OKBLUE+"]"+bcolors.HEADER+"1 Hour\n"+bcolors.OKBLUE+"["+bcolors.OKGREEN+"3"+bcolors.OKBLUE+"]"+bcolors.HEADER+"1 Day\n"+bcolors.OKBLUE+"["+bcolors.OKGREEN+"4"+bcolors.OKBLUE+"]"+bcolors.HEADER+"1 Month\n"+bcolors.OKBLUE+"["+bcolors.OKGREEN+"5"+bcolors.OKBLUE+"]"+bcolors.HEADER+"Never\n"+bcolors.CYAN+"==> "+bcolors.OKGREEN)
        if expiration == "5":
            expiration = "never"
    while syntax not in syntaxes:
        syntax = raw_input(bcolors.OKBLUE+"\n["+bcolors.OKGREEN+"*"+bcolors.OKBLUE+"] "+bcolors.HEADER+"Enter the language syntax "+bcolors.OKBLUE+"["+bcolors.WARNING+"?"+bcolors.OKGREEN+" to see available syntax"+bcolors.OKBLUE+"]"+bcolors.HEADER+":\n"+bcolors.CYAN+"==> "+bcolors.OKGREEN)
        if syntax =="?":
            for a in syntaxes:
                print a
    Mythread = unixhubuploader(title, paste, exposure, expiration, syntax)
    Mythread.start()




if __name__ == "__main__":
    if len(argv)!= 1:
        if argv[1]=="-c" or argv[1]=="--CLI" or argv[1]=="--cli":
            menu()
        else:
            if len(argv) != 11:
                print "Usage: \nunixhubPASTE.py -t title -p paste_doc -e exposure -ex expiration -s syntax\nunixhubPASTE.py --cli #for the cli version"
            else:
                new = ""
                for c in argv:
                    new+= c+" "
                mytitle      = re.findall("-t ([^-]+)", new)[0].replace(" ","")
                mypaste      = open(re.findall("-p ([^-]+)", new)[0].replace(" ","")).read()
                myexposure   = re.findall("-e ([^-]+)", new)[0].replace(" ","")
                myexpiration = re.findall("-ex ([^-]+)", new)[0].replace(" ","")
                mysyntax     = re.findall("-s ([^-]+)", new)[0].replace(" ","")
                if myexpiration == '10min':
                    myexpiration='1'
                elif myexpiration =='1h':
                    myexpiration='2'
                elif myexpiration == '1day':
                    myexpiration='3'
                elif myexpiration =='1month':
                    myexpiration='4'
                elif myexpiration =='never':
                    myexpiration='never'

                Mythread = unixhubuploader(mytitle, mypaste, myexposure, myexpiration, mysyntax)
                Mythread.start()
    else:
        print "Usage: \nunixhubPASTE.py -t title -p paste_doc -e exposure -ex expiration -s syntax\nunixhubPASTE.py --cli #for the cli version"


