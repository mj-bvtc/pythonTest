import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
import datetime
import socket
import threading

## import raspberry pi GPIO Library ##
if(str(os.name)=="posix"):
    import RPi.GPIO as GPIO;

class BVTC_Email():
    def __init__(self, auth_user=None, auth_pass=None, send_as = None):
        self.cxn = smtplib.SMTP()
        self.server = 'smtp.office365.com'
        self.port = 587

        self.user = auth_user;
        self.password = auth_pass;
        if(send_as): self.sendAs = send_as;
        else: self.sendAs = self.user;

        if(self.user and self.password): self.login();

    def login(self, auth_user=None, auth_pass=None):
        if(auth_user and auth_pass):
            self.user = auth_user;
            self.password = auth_pass;

        self.cxn.connect(self.server, self.port)
        self.cxn.starttls()
        self.cxn.login(self.user, self.password)

    def send_email(self, to, message, subject = "",send_as=None, close=True):
        msg = MIMEMultipart();
        
        ##  if sender is not provided, use authenticated user ##
        if(send_as): msg['From'] = send_as;
        else: msg['From'] = self.sendAs;
        msg['From'] = self.sendAs;

        msg['To'] = to;
        if(subject):
            msg['Subject'] = subject;
        msg.attach(MIMEText(message, 'plain'));

        try:
            mail = self.cxn.sendmail(self.sendAs, to, msg.as_string())
        except: raise
            #print ("Error sending email.");
        if(close): self.logout()

    def logout(self):
        self.cxn.quit()

class RaspiMonitor():
    def __init__(self, email_authUser = "", email_authPassword = "", email_sender=""):
        
        self.ThreadedEmails = False;

        self.pullDownPins = [];
        self.pullDownNames = [];
        self.lastStates=[];

        self.EmailList = [];
        self.deviceName = socket.gethostname();
        
        self.Running = False;
        
        self.logPath = os.path.join(os.path.abspath("."), "log.txt")
        print(self.logPath);

        ## store email credintials ##
        self.Mail_AuthUser = email_authUser;
        self.Mail_AuthPassword = email_authPassword;
        if(email_sender): self.Mail_SendAs = email_sender;
        else:self.Mail_SendAs = self.Mail_AuthUser;

    def Add_Pulldown(self, pin, name):
        self.pullDownPins.append(pin);
        self.pullDownNames.append(name);
        self.lastStates.append(None);

        GPIO.setmode(GPIO.BCM);
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def Start(self):
        self.Running = True;
        self.RunMonitor();

    def EmailCreds(self, user, password, sendAs = ""):
        self.Mail_AuthUser = user;
        self.Mail_AuthPassword = password;
        if(sendAs): self.Mail_SendAs = sendAs;
        else:self.Mail_SendAs = self.MailUser;

    def RunMonitor(self, delay = 1):
        while (self.Running):
            try:
                for i in range(len(self.pullDownPins)):
                    pin = self.pullDownPins[i]
                    lastState = self.lastStates[i];
                    name = self.pullDownNames[i];

                    ## check state##
                    input_state = GPIO.input(pin);

                    ## Send update email ##
                    if(lastState == None):
                        if(self.ThreadedEmails): threading._start_new_thread(self.StartupEmail, (name, pin));
                        else: self.StartupEmail(name, pin);
                        sleepThread = True;
                    elif(lastState != input_state):
                        if(self.ThreadedEmails): threading._start_new_thread(self.EmailAlert, (input_state, name));
                        else: self.EmailAlert(name, pin);
                        sleepThread = True;
                    else:
                        sleepThread = False;
                
                    ## set the current state in the list ##
                    self.lastStates[i] = input_state;
                    if(sleepThread): time.sleep(1);
                
                ## delay between loops to not overheat raspberrypi ##
                if(delay > 0): time.sleep(1);
            except:
                GPIO.cleanup();

    def EmailAlert(self, state, name):
        if(state): DeviceStatus="OFF";
        else: DeviceStatus="ON";

        ## compose email ##
        title = self.deviceName + " " + name + " " + DeviceStatus

        if (state):
            message = self.deviceName.split("-")[0] + " alarm has been stopped.";
        else:
            message = self.deviceName.split("-")[0] + " alarm code!";
        self.WriteToLog(message);

        ## send email to alert list ##
        email = BVTC_Email(self.Mail_AuthUser, self.Mail_AuthPassword, self.Mail_SendAs);
        for sendTo in self.EmailList:
            email.send_email(sendTo, message, title, close=False);
        email.logout()
        
    def StartupEmail(self, name, pin):
        title = self.deviceName + " Monitoring"
        message = "Starting to listen for " + name + "(s) on pin: " + str(pin);
        self.WriteToLog(message)

        ## send email to alert list ##
        email = BVTC_Email(self.Mail_AuthUser, self.Mail_AuthPassword, self.Mail_SendAs);
        for sendTo in self.EmailList:
            email.send_email(sendTo, message, title, close=False);
        email.logout();

    def WriteToLog(self, message):
        try:
            timestamp = datetime.datetime.now.strftime("%Y-%m-%d %H:%M:%S")
            with open(self.logPath, "a") as myfile:
                myfile.write(timestamp + "--" + message + "\n ");
        except: pass


if __name__ == "__main__":  
    auth_user = "xerox@bostonvalley.com"
    auth_pass = "bvtcX3r0x"
    sendAs = "it@bostonvalley.com"

    ## Raspberry Pi ##
    if(os.name == "posix"):
        monitor = RaspiMonitor(auth_user, auth_pass,sendAs)
        monitor.Add_Pulldown(21, "Alarm")
        monitor.EmailList.append("7162886426@vzwpix.com"); # Pete 
        monitor.EmailList.append("peters@bostonvalley.com");
        #monitor.EmailList.append("5853136498@vzwpix.com"); # Andrew
        #monitor.EmailList.append("7164355449@vzwpix.com"); # Richard
        #monitor.EmailList.append("7169826970@vzwpix.com"); # Craig K
        #monitor.EmailList.append("7165746371@vzwpix.com"); # Gary
        monitor.Start()
    elif(os.name == "nt"):
        ## test email procedure ##
        monitor = RaspiMonitor(auth_user, auth_pass,sendAs)
        monitor.EmailList.append("7162886426@vzwpix.com"); # Pete
        monitor.EmailList.append("5853136498@vzwpix.com"); # Andrew
        monitor.EmailList.append("peters@bostonvalley.com");
        monitor.StartupEmail("Test-raspi", 21)
        #monitor.EmailAlert(False, "Test-raspi")



