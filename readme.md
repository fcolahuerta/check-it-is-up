# check it is up #

Is a simple python script that can be run in a LAMP linux server.
Checks in a LAMP server if a web is accesible.
If not restart the services and make a copy of the last lines of the log files.

Very useful when services keep crashing and you want to keep running it no matter what.

Use it under your own criteria.

## Functions ##

In the server were it runs check if a web url is accesible.

If not restart the services and make a copy of the last lines of the log files.

## Checking the web ##

To check the web via Beautiful soup finds a meta tag and compared with a value.
If the comparison is not succesful then

  * It makes a copy of the last lines of the apache log and mysql
  * Restart the services of the LAMP server

> Example:
> > To a objective web url  the following meta line can be added in the header
```
    <meta name="check_it_is_up" content="check_it_is_up_key_value">
```
## Dependencies ##


> Python 2.7

> urllib2

> Beatifulsoup
```
      sudo apt-get install python-beautifulsoup
```

## Configuration cronjobs ##

The script is run as a cronjob with root privileges

Cronjobs installation:

> add the followin line to cronjobs
```
    >>$ sudo crontab -e
```
> add the following line (the script will be run evert 2 mins.
```
        */2 * * * * python <path to the folder>/check_is_up.py
```
## Configuration check\_is\_up.py ##

The configuration is done in the main file check\_is\_up.py first function main()

Block options, declare which sevices want to be restarted. A pre and post bash files
can be run it (_check\_is\_up\_pre.bh_ and _check\_is\_up\_post.bh_).
```
    check_it_is_up.action.options(runBash = False , 
                                   MYSQL = True,
                                   MUNIN = True,
                                   APACHE = True,
                                   VARNISH = True,
                                   SpamASASSIN = True,
                                   POSTFIX = True,
                                   runBash_post = False,
                                   disk_usage = True)
     
```


Block logs, declare which logs want to be readed, and the route
```
    check_it_is_up.action.log_options(log_APACHE = "/var/log/apache2/error.log",
                                      log_MySQL = "/var/log/mysql.log")   
```

Block add web, adds a url to check via the title
```
    check_it_is_up.add_web_to_check(name = "name", 
                                     url = "http://www.yourweb.com",
                                     key = "title",
                                     key_result = "Title value") 
```
Block add meta tag, adds a url to check via the header meta tag check\_it\_is\_up
```
    check_it_is_up.add_web_to_check_meta_tag(name = "name_meta", 
                                             url = "http://www.yourweb.com")      
```
## Security ##

It is convinient to secure the scripts as root user

to secure
```
>>$ sudo bash as_root.bh
```

to edit
```
>>$ sudo bash un_root.bh
```

## Log file output ##
A subfolder /log is created

The log files contain the info of each time check it is up has been run
and the apache and mysql log files info.

