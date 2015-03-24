from requests import session
from bs4 import BeautifulSoup

def makerequest(webmailid,password):
	'''with session() as c:
		#c.get('https://www.google.co.in/?gws_rd=ssl')
		#print "Booya!"
		payload = {'loginOp': 'login', 'username': webmailid, 'password': password,'client': 'preferred'}
		c.get('https://webmail.daiict.ac.in')
		c.post('https://webmail.daiict.ac.in/zimbra/', data=payload)
		request = c.get('https://webmail.daiict.ac.in/zimbra/')	
		html = request.text.encode('utf-8')
		soup = BeautifulSoup(html)
		title= soup.title
		print title

		if "DA-IICT Webmail Log In" in title:
			string = "False"
		else:
			string = "True"

		print string
		
		try:
			req = c.get("https://webmail.daiict.ac.in/zimbra/h/search?mesg=welcome&initial=true&app=")
			string = "True"
			print req.status_code
			#print req.text
		except:
			string = "False"

		print string'''
		
	return "True"