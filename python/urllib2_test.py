import urllib
import urllib2


token="fCdPRD1ZF4N89Wrx3-47ohuONZ1eyB72ar9HHmlkEjFe4G-ECkViWaRHnWQyIocX-pEnpQks1ouzbVw3G6Pzfk5MwkXQGTr2KGgncOXwvOI"
url="https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=%s" %  token
print urllib2.urlopen(url).read()
