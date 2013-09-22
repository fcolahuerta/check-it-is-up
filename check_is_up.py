#!/usr/bin/env python

###
### check it is up
###
### License: GNU GPL v3
### Author: FLC 2013
###
### Simple python script that
### can be run in a web LAMP linux server.
###
##################################

import urllib2
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import subprocess
import os
import logging
import logging.handlers

"""
    Main function to run
    ###########################

"""

def main():
    
    ###  Main function
    ###     Declare actions to run
    ###     Add urls and tests
    
    check_it_is_up = check_is_up()
    
    ### Declare the actions to run
    check_it_is_up.action.options(runBash = False , 
                                   MYSQL = True,
                                   MUNIN = True,
                                   APACHE = True,
                                   VARNISH = True,
                                   SpamASASSIN = True,
                                   POSTFIX = True,
                                   runBash_post = False,
                                   disk_usage = True)
    
    ### Declare the logs to copy
    check_it_is_up.action.log_options(log_APACHE = "/var/log/apache2/error.log",
                                      log_MySQL = "/var/log/mysql.log")    
    
    ### Declare webs to check
    """
    check_it_is_up.add_web_to_check(name = "name", 
                                     url = "http://www.yourweb.com",
                                     key = "title",
                                     key_result = "Title value")
    """                                    
    check_it_is_up.add_web_to_check_meta_tag(name = "name_meta", 
                                             url = "http://www.yourweb.com")                                                                           
    
    ### Check it
    check_it_is_up.check_are_up()
    
    return

"""
    check_is_up object
    ###########################

"""

class check_is_up(object):

    ###  Main class
    ###     Check for a url if a web available
    ###     Compares key tag value with its text
    ###     From BeautifulSoup soup.find( txt_key ).getText() is used
    ###     If the comparison is not possible runs an action

    def __init__(self):
        
        ### Options
        self.__version__ = "0.1"
        self._debug = False
        self._force_error = True
        
        if self._debug == False: self._force_error = False
        
        ### Main variables
        self._names = []
        self._urls = []
        self._key = []
        self._key_result = []
        
        ### Log object
        self.log = _log(self)
        self.log._log_file = "_check_is_up.log"
        
        ### Action object
        self.action = _action(self)
        
    def add_web_to_check(self, name, url, key, key_result):
    
        ### Add web to check variables
        ###     
    
        if name == "" or url == "" or key == "" or key_result == "":
            
            self.log.warning("Add web to check. Not allowed empty fields.")
            return False
        
        self._names.append(name)  
        self._urls.append(url)
        self._key.append(key)
        self._key_result.append(key_result)
        
    def add_web_to_check_meta_tag(self, name, url, key="check_it_is_up", key_result="check_it_is_up_key_value"):
    
        ### Add web to check variables
        ###     
    
        if name == "" or url == "" or key_result == "" or key == "":
            
            self.log.warning("Add web to check. Not allowed empty fields.")
            return False
        
        self._names.append(name)  
        self._urls.append(url)
        self._key.append(key)
        self._key_result.append(key_result)        
        
        
    def check_are_up(self):
    
        ### Runs the proof check
        ###    
               
        if len(self._names) == 0:
            return
        
        if self._debug:
            self.log.info("----- check is up v%s" % self.__version__)
            self.log.info("----- Debug mode")
                
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}
        proof = True
        ii = 0
        
        ### Check all the urls
        for ii in range(0,len(self._names)):
            
            url = self._urls[ii]
            answer = self._key_result[ii]      
            key_tag = self._key[ii]      
            
            try:
                
                req = urllib2.Request(url,None,headers)
                page = urllib2.urlopen(req)

                soup = BeautifulSoup(page)
                
                if key_tag == "check_it_is_up":
                    self.log.info("Check it is up meta %s" % url)
                    key = soup.find("meta", {"name":key_tag})['content']                
                else:
                    self.log.info("Check it is up %s" % url)
                    key = soup.find(key_tag).getText()
                
                if key == answer:
                    ### Positive proof    
                    proof = True
                    self.log.info("    Is up")
                    
                else:
                    ### Negative proof
                    proof = False
                    self.log.warning("    Key error")
                    break
                    
            except:
                ### Negative proof
                proof = False
                self.log.info("    Retrive error")
                break
                
        ### Run action                
        if os.getuid() != 0:
            
            self.log.warning("To run actions root privilages are required")
            
        else:    
            
            if not proof or self._force_error:
                
                if self._force_error: self.log.warning("Force actions")
                
                self.action.run_action(proof)
                   
    
"""
    Log object
    ###########################

"""    

class _log(object):
    
    ###  Log object
    ###  Builds up the log file
    
    def __init__(self, parent):             
        
        ### Initialise log object 
        ### 
        
        self.parent = parent
        
        self._debug = self.parent._debug      
        
        self._log_file = "_check_is_up.log"
        
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "log","")
        self._assure_path_exists(path)
        path = os.path.join(path, self._log_file)
        
        self.logger = logging.getLogger('check_is_up')
        #self.hdlr = logging.FileHandler(path)
        self.hdlr = logging.handlers.RotatingFileHandler(path, maxBytes=10**5, backupCount = 6)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(formatter)
        self.logger.addHandler(self.hdlr) 
        self.logger.setLevel(logging.INFO)        

    def _assure_path_exists(self, path):
    
        ### Initialise log object 
        ###             
        dirr = os.path.dirname(path)
        if not os.path.exists(dirr):
            os.makedirs(dirr)
            print "Log folder created %s" % dirr
                
    def info(self, msg):
        
        print msg
        self.logger.info(msg) 
        
    def warning(self, msg):
        
        print msg
        self.logger.warning(msg)           
    
    
"""
    Action object
    ###########################

"""        
class _action(object):
    
    ###  Action object
    ###     Runs an action when proof is True
    
    def __init__(self, parent):             
        
        ### Initialise object 
        ###     All actions are off
        
        self.parent = parent
        
        self._debug = self.parent._debug
        self.log = self.parent.log
              
        default = False
        
        ### Action
        self.runBash = default
        self.MYSQL = default
        self.MUNIN = default
        self.APACHE = default
        self.VARNISH = default
        self.SpamASASSIN = default
        self.POSTFIX = default
        self.runBash_post = default
        self.disk_usage = default
        
        ### Log files read
        self.log_APACHE = default
        self.log_MySQL = default
        
    def options(self, runBash = False , MYSQL = False, MUNIN = False, APACHE = False, \
                      VARNISH = False, SpamASASSIN = False, POSTFIX = False, runBash_post = False, \
                      disk_usage = False):
        
        ### Change the state of the action
        ### 
        
        self.runBash = runBash
        
        self.MYSQL = MYSQL
        self.MUNIN = MUNIN
        self.APACHE = APACHE
        self.VARNISH = VARNISH
        self.SpamASASSIN = SpamASASSIN
        self.POSTFIX = POSTFIX    
        self.runBash_post = runBash_post        
        self.disk_usage = disk_usage
        
    def log_options(self, log_APACHE = "", log_MySQL = ""):
        
        ### Change the state of the log read action
        ###
        
        def check(log):
        
            if log == "":
                return False, ""
                
            else:
                if os.path.isfile(log):
                    return True, log
                else:
                    self.log.warning( "Log file path not correct %s" % log )
                    return False, ""
        
        ### Assign values
        self.log_APACHE, self.log_path_APACHE = check( log_APACHE )
        self.log_MySQL, self.log_path_MySQL = check( log_MySQL )

        
    def run_action(self, proof = True):
    
        ### Run actions
        ###
        
        def _console_run( case, text, cmd, debug = False ):
            ### run process
            
            def cmd_process(cmd, text):
                ### run process
                process = subprocess.Popen( cmd , stdout=subprocess.PIPE)
                out_prc, err = process.communicate()                    
                
                out = text + "\n"
                out = out + out_prc
                
                self.log.info( out )            
            
            ############
            
            if case:
            
                #self.log.info( text )
                
                if self._debug == False:
                    
                    cmd_process(cmd, text)
                    
                else:
                    
                    if debug:
                        
                        cmd_process(cmd, text)
                    
        ############
        
        if os.getuid() != 0:
            self.log.warning( "Actions run require root privilages" )
            return False
                
        if proof == True and not self.parent._force_error:
                       
            return True
        
        else:
            
            if self.parent._force_error: print "Force actions"
            
            self._read_log(self.log_APACHE,
                           log_name = "******** Last Apache log lines before actions" , 
                           log_path = self.log_path_APACHE,
                           window=20 )
                           
            self._read_log(self.log_MySQL,
                           log_name = "******** Last MySQL log lines before actions" , 
                           log_path = self.log_path_MySQL,
                           window=20 )                           
            
            _console_run( self.runBash, 
                          "******** Run pre bash file",
                          ["bash","_check_is_up_pre.bh"] )         
            
            _console_run( self.MYSQL, 
                          "******** MYSQL status",
                          ["service","mysql","status"] )             
            
            _console_run( self.MYSQL, 
                          "******** MYSQL restart",
                          ["service","mysql","restart"] )       
            
            _console_run( self.MUNIN, 
                          "******** Munin status",
                          ["service","munin-node","status"] )             
            
            _console_run( self.MUNIN, 
                          "******** Munin restart",
                          ["service","munin-node","restart"] )         
            
            _console_run( self.APACHE, 
                          "******** Apache2 status",
                          ["service","apache2","status"] )            
            
            _console_run( self.APACHE, 
                          "******** Apache2 restart",
                          ["service","apache2","restart"] )  
                          
            _console_run( self.VARNISH, 
                          "******** Varnish status",
                          ["service","varnish","status"] )                          
                          
            _console_run( self.VARNISH, 
                          "******** Varnish restart",
                          ["service","varnish","restart"] )                         

            _console_run( self.SpamASASSIN, 
                          "******** SpamAsassin status Amavis",
                          ["/etc/init.d/amavis","status"] )
                          
            _console_run( self.SpamASASSIN, 
                          "******** SpamAsassin restart Amavis",
                          ["/etc/init.d/amavis","restart"] )                                                                                      

            _console_run( self.POSTFIX, 
                          "******** Postfix status",
                          ["service","postfix","status"] ) 

            _console_run( self.POSTFIX, 
                          "******** Postfix restart",
                          ["service","postfix","restart"] ) 
                          
            _console_run( self.runBash_post, 
                          "******** Run post bash file",
                          ["bash","_check_is_up_post.bh"] )    
                          
            _console_run( self.disk_usage, 
                          "******** Disk usage",
                          ["df","-h","/"],
                          debug = self._debug )                                                 
   
            return True
            
    def _read_log(self, case , log_name , log_path, window=20):
        
        ### Check active
        if not case: return False
        
        ### Read the last lines of a log file
        try:
            f = open(log_path,"r")
        except:
            self.log.warning( "Not possible to open log file %s" % log_path )
            return False

        txt_end = self._tail( f, window=window )   
                
        f.close()
        
        ### log it
        out = log_name + "\n"
        out = out + txt_end
        
        self.log.info( out )         
        
        return True
        
    def _tail( self, f, window=20 ):
        ### Peak the las lines
        ### http://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail
    
        BUFSIZ = 2048
        f.seek(0, 2)
        bytes = f.tell()
        size = window
        block = -1
        data = []
        
        while size > 0 and bytes > 0:
            
            if (bytes - BUFSIZ > 0):
                # Seek back one whole BUFSIZ
                f.seek(block*BUFSIZ, 2)
                # read BUFFER
                data.append(f.read(BUFSIZ))
            else:
                # file too small, start from begining
                f.seek(0,0)
                # only read what was not read
                data.append(f.read(bytes))
                
            linesFound = data[-1].count('\n')
            size -= linesFound
            bytes -= BUFSIZ
            block -= 1
            
        return '\n'.join(''.join(data).splitlines()[-window:])        
              
        
        

#### Run    
main()    

