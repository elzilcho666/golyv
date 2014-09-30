from flask import Flask, render_template, request, make_response
from libadam.db import adamDB
from OpenSSL import SSL
import libadam.simple_enc
import json, MySQLdb, magic, hashlib, datetime
enc = libadam.simple_enc.simple_encryption()
class settings:
	def __init__(self):
		settings = json.loads(open('settings.json', 'r').read())
		self.ip = settings['ip']
		self.port = settings['port']
		self.user = settings['user']
		self.password = settings['password']
		self.sslkey = settings['sslkey']
		self.sslcert = settings['sslcert']
		self.db = settings['db']
s = settings()
'''
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file(s.sslkey)
context.use_certificate_file(s.sslcert)
'''
imagefiles = ['PNG ', 'GIF ', 'JPEG']
app = Flask(__name__)
#codes:
# 0 = everything is fine, requested data should be in the request
# 1 = no data to show
# 2+ = various errors I will encount, I may update

class events(adamDB):
	# events is an array of dicts and seperate json output of same
	# json funct would act like this object.listevents_json ->
	# call self.listevents -> return data to self.json -> encode json
	# -> return output
	def listevents(self):
		sql = "SELECT * FROM events"
		results = []
		for row in self.execute(sql):
			result = {}
			result['id'] = row[0]
			result['title'] = row[1]
			result['time'] = row[2]
			result['date'] = row[3]
			result['price'] = row[4]
			result['description'] = row[5]
			result['image_hash'] = row[6]
			result['host'] = row[7]
			result['event_type'] = row[8]
			result['address'] = row[9]
			result['lat'] = row[10]
			result['lon'] = row[11]
			results.append(result)
		return results
	def event_info(self, event_id):
		sql = "SELECT * FROM events WHERE event_id='%s'" % (self.sanitize(event_id))
		for row in self.execute(sql):
			result = {}
			result['title'] = row[1]
			result['time'] = row[2]
			result['date'] = row[3]
			result['price'] = row[4]
			result['description'] = row[5]
			result['image'] = row[6]
			result['host'] = row[7]
			result['address'] =row[9]
			return result
	def listevents_json(self):
		return json.dumps(self.listevents())
	def addevent(self, time, event_day, event_month, event_year, title, price, description, image, host, event_type, address1='', address2='', town='', postcode='', country='', lat=0, lon=0):
		sql = "INSERT INTO events(time, event_day, event_month, event_year, title, price, description, image_hash, host, event_type, address, lat, lon) VALUES('%s', '%s', %s, %s, %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s);" % (self.sanitize(time), self.sanitize(event_day), self.sanitize(event_month), self.sanitize(event_year), self.sanitize(title), self.sanitize(price), self.sanitize(description), self.sanitize(image), self.sanitize(host), self.sanitize(event_type), self.sanitize(address1), self.sanitize(address2), self.sanitize(town), self.sanitize(postcode), self.sanitize(country), self.sanitize(lat), self.sanitize(lon))
		print sql
		self.execute(sql, True) 
		return 'done'
class users(adamDB):
	def login(self, username, password):
		now = datetime.datetime.now() + datetime.timedelta(days=30)
		if(self.verify_password(username, password)):
			key = {}
			key['challenge'] = enc.encrypt(hashlib.sha224(password).hexdigest(), now.strftime('%d/%m/%Y %H:%M:%S'))
			key['status'] = 'success'
			return key
		key = {}
		key['status'] = 'failure'
		return key
	def register(self, username, password, firstname, surname, email, gender, dob_day, dob_month, dob_year, address1, address2, town, postcode, country, facebook, twitter, instagram, forgot_p_q, forgot_p_a, caption = "I'm a new user.", extrainfo = json.dumps('{}')):
		password = hashlib.sha224(password).hexdigest()
		sql = "INSERT INTO users(username, password, firstname, surname, email, gender, dob_day, dob_month, dob_year, address1, address2, town, postcode, country, facebook, twitter, instagram, forgot_p_q, forgot_p_a, caption, extrainfo) VALUES('%s', '%s', '%s', '%s', '%s', '%s', %s, %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (self.sanitize(username), self.sanitize(password), self.sanitize(firstname), self.sanitize(surname), self.sanitize(email), self.sanitize(gender), self.sanitize(dob_day), self.sanitize(dob_month), self.sanitize(dob_year), self.sanitize(address1), self.sanitize(address2), self.sanitize(town), self.sanitize(postcode), self.sanitize(country), self.sanitize(facebook), self.sanitize(twitter), self.sanitize(instagram), self.sanitize(forgot_p_q), self.sanitize(forgot_p_a), self.sanitize(caption), self.sanitize(extrainfo))
		self.execute(sql, True)
	def verify_password(self, user, password):
		sql = "SELECT password FROM users WHERE username='%s'" % (self.sanitize(user))
		for row in self.execute(sql):
			if hashlib.sha224(password).hexdigest() == row[0]:
				return True
		return False
	def verify_challenge(self, user, challenge):
		sql = "SELECT password FROM users WHERE username='%s'" % (self.sanitize(user))
		challenge_token = {}
		for row in self.execute(sql):
			decrypted_challenge = enc.decrypt(row[0], challenge)
			challenge_date = ''
			try:
				challenge_date = datetime.datetime.strptime(decrypted_challenge, '%d/%m/%Y %H:%M:%S')
			except:
				challenge_token['status'] = 'bad_challenge'
				return challenge_token
			now = datetime.datetime.now()
			if(challenge_date > now):
				challenge_token['status'] = 'success'
				return challenge_token
			else:
				challenge_token['status'] = 'expired_challenge'
				return challenge_token
		challenge_token['status'] = 'unknown_error'
		return challenge_token
	def update_caption(self, user, caption):
		sql = "UPDATE users SET caption='%s' WHERE username='%s'" % (self.sanitize(caption), self.sanitize(user))
		self.execute(sql)
	def my_events(self, user):
		pass
	def update_info(self, user, password, info):
		#update info will be in json so that unchanged values can be preserved
		pass
	def get_user_id(self, user):
		sql = "SELECT user_id FROM users WHERE username='%s'" % (self.sanitize(user))
		for row in self.execute(sql):
			return row[0]
	def cancel_membership(self, user, password):
		sql = "DELETE FROM users WHERE username='%s'" % (user)
		if(self.verify_password(user, password)):
			self.execute(sql, True)
	def user_lookup(self, user):
		sql = "SELECT user_id, username, caption, town FROM users WHERE username='%s'" % (self.sanitize(user))
		for row in self.execute(sql):
			condensed_user_info = {}
			condensed_user_info['user_id'] = row[0]
			condensed_user_info['user'] = row[1]
			condensed_user_info['status'] = row[2]
			condensed_user_info['city'] = row[3]
			return condensed_user_info

#class rsvps(adamDB):

e = events(s.ip, s.port, s.user, s.password, s.db)
u = users(s.ip, s.port, s.user, s.password, s.db)
#e.addevent('4:00pm', '21/06/1991', 'My Birthday', '$24', 'Massive birthday bash', 'no image', 'Adam Jeanes', 'Private', '208 South Victoria Road, Dundee, DD1 3BF')
@app.route('/')
def index():
	return render_template('index.html')
@app.route('/img', methods=['POST'])
def image():
	imgfile = request.files['file']
@app.route('/post')
def post():
	username = request.cookies.get('username')
	challenge_key = request.cookies.get('challenge_key')
	challenge_token = u.verify_challenge(username, challenge_key)
	if challenge_token['status'] == 'success':
		return render_template('post.html')
	return render_template('login.html')
@app.route('/evnts')
def newevents():
	return e.listevents_json()
@app.route('/viewevents')
def viewevents():
	username = request.cookies.get('username')
	challenge_key = request.cookies.get('challenge_key')
	challenge_token = u.verify_challenge(username, challenge_key)
	if challenge_token['status'] == 'success':
		return render_template('viewevents.html', events=e.listevents())
	return render_template('login.html')
@app.route('/event/<int:event_id>')
def view_event(event_id):
	username = request.cookies.get('username')
	challenge_key = request.cookies.get('challenge_key')
	challenge_token = u.verify_challenge(username, challenge_key)
	if challenge_token['status'] == 'success':
		return render_template('eventinfo.html', event=e.event_info(event_id))
	return render_template('login.html')
@app.route('/newevnt', methods=['POST'])
def newevent():
	appdataob = request.json
	appdataob['image'] = 'n/a'
	appdataob['event_day'] = appdataob['date'].split('/')[0]
	appdataob['event_month'] = appdataob['date'].split('/')[1]
	appdataob['event_year'] = appdataob['date'].split('/')[2]
	if appdataob['address1']:
		e.addevent(appdataob['time'], appdataob['event_day'], appdataob['event_month'], appdataob['event_year'], appdataob['title'], appdataob['price'], appdataob['description'], appdataob['image'], appdataob['host'], appdataob['event_type'], appdataob['address1'], appdataob['address2'], appdataob['town'], appdataob['postcode'], appdataob['country'])
		return json.dumps({'status':'ok'})
	elif appdataob['lat']:
		if appdataob['lon']:
			e.addevent(appdataob['time'], appdataob['date'], appdataob['title'], appdataob['price'], appdataob['description'], appdataob['image'], appdataob['host'], appdataob['event_type'], appdataob['address'], appdataob['lat'], lon['lon'])
			return json.dumps({'status':'ok'})
	return 'needs a location (address or gps coordinates)'

@app.route('/static/<path:filename>')
def staticfile(filename):
	f = open('/static/' + filename, 'R')
	return f.read()
@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		#username, password, firstname, surname, email, gender, dob_day, dob_month, dob_year, address1, address2, town, postcode, country, facebook, twitter, instagram, forgot_p_q, forgot_p_a, caption = "I'm a new user.", extrainfo = json.dumps('{}')):
		userOb = request.json
		u.register(userOb['username'], userOb['password'], userOb['firstname'], userOb['surname'], userOb['email'], userOb['gender'], userOb['birthday'], userOb['birthmonth'], userOb['birthyear'], userOb['address1'], userOb['address2'], userOb['town'], userOb['postcode'], userOb['country'], 'tbd', 'tbd', 'tbd', userOb['forgot_p_q'], userOb['forgot_p_a'])
		
		return 'not implemented yet'
	else:
		return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():

	if request.method == 'POST':
		login_token = u.login(request.json['username'], request.json['password'])
		if login_token['status'] == 'success':
			print 'successful login for %s' % (request.json['username'])
			response = make_response(json.dumps(login_token))
			response.set_cookie('challenge_key', login_token['challenge'])
			response.set_cookie('username', request.json['username'])
			return response
		print 'failed login'
		return json.dumps(login_token)
	else:
		return render_template('login.html')
@app.route('/donereg')
def done_registration():
	return render_template('donereg.html')
@app.route('/<string:username>/home')
def homepage(username):
	challenge_key = request.cookies.get('challenge_key')
	challenge_token_result = u.verify_challenge(username, challenge_key)
	if challenge_token_result['status'] == 'success':
		return render_template('home.html')
	else:
		return render_template('login.html')
	return json.dumps(challenge_token_result)
@app.route('/logout')
def logout():
	response = make_response(render_template('logout.html'))
	response.set_cookie('challenge_key', '', expires=0)
	response.set_cookie('username', '', expires=0)
	return response
@app.route('/<string:user>/settings')
def settings_main(user):
	challenge_key = request.cookies.get('challenge_key')
	challenge_token = u.verify_challenge(user, challenge_key)
	if challenge_token['status'] == 'success':
		return render_template('settingsmain.html')
	return render_template('login.html')
@app.route('/<string:user>/settings/caption')
def settings_caption(user):
	challenge_key = request.cookies.get('challenge_key')
	challenge_token = u.verify_challenge(user, challenge_key)
	if challenge_token['status'] == 'success':
		return render_template('settingscaption.html')
	return render_template('login.html')
@app.route('/<string:user>/settings/editprofile')
def settings_editprofile(user):
	challenge_key = request.cookies.get('challenge_key')
	challenge_token = u.verify_challenge(user, challenge_key)
	if challenge_token['status'] == 'success':
		return render_template('')
	return render_template('login.html')
@app.route('/<string:user>/settings/closeaccount', methods=['GET', 'POST'])
def settings_closeaccount(user):
	challenge_key = request.cookies.get('challenge_key')
	challenge_token = u.verify_challenge(user, challenge_key)
	if challenge_token['status'] == 'success':
		if request.method == 'POST':
			json = request.json
			if u.verify_password(user, json['password']):
				u.cancel_membership(user, json['password'])
				return 'account deleted'
			return 'account not deleted'
		return render_template('settingscancel.html')
	return render_template('login.html')
@app.route('/<string:user>/settings/accountclosed')
def settings_closedaccount(user):
	render_template('')
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True) #, ssl_context=context


