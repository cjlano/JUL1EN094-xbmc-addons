# -*- coding: utf-8 -*-   
#---------------------------------------------------------------------
"""
debridroutine python library
Copyright (C) 2013 JUL1EN094

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import urllib, urllib2
import re, os, cookielib

class RealDebrid:

    def __init__(self, cookie_file, username, password):
        self.cookie_file = cookie_file
        self.username = username
        self.password = password
        


    def GetURL(self, url):

        print 'DebridRoutines - Requesting URL: %s' % url
        if self.cookie_file is not None and os.path.exists(self.cookie_file):
            cj = cookielib.LWPCookieJar()
            cj.load(self.cookie_file)
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            response = opener.open(req)

            #check if we might have been redirected (megapremium Direct Downloads...)
            finalurl = response.geturl()

            #if we weren't redirected, return the page source
            if finalurl is url:
                link=response.read().replace('|','&&&').replace('\\','')
                response.close()
                return link

            #if we have been redirected, return the redirect url
            elif finalurl is not url:
                return finalurl


    def Resolve(self, url, quality):
        print 'notice here:'+url
        print 'DebridRoutines - Resolving url: %s' % url
        url = 'http://www.real-debrid.com/ajax/unrestrict.php?link=' + url
        source = self.GetURL(url)
        print 'DebridRoutines - Returned Source: %s' % source
        link = re.search('"'+quality+'","(.+?)"', source).group(1)
        return link


    def valid_host(self, host):
        try :
            url = 'http://www.real-debrid.com/api/regex.php?type=all'
            response = self.GetURL(url).lstrip('/').rstrip('/g')
            delim = '/g,/|/g\|-\|/'
            allhosts = [re.compile(host) for host in re.split(delim, response)]
            if host in allhosts:
                return True
            else:
                return False            
        except:
            return False


    def checkLogin(self):
        url = 'https://real-debrid.com/api/account.php'
        source = self.GetURL(url)
        if source is not None and re.search('expiration', source):
            return False
        else:
            return True


    def Login(self):
        if self.checkLogin():
            cj = cookielib.LWPCookieJar()
            login_data = urllib.urlencode({'user' : self.username, 'pass' : self.password})
            url = 'https://real-debrid.com/ajax/login.php?' + login_data
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

            #do the login and get the response
            response = opener.open(req)
            source = response.read()
            response.close()
            cj.save(self.cookie_file)
            print source
            if re.search('OK', source):
                return True
            else:
                return False
        else:
            return True
 