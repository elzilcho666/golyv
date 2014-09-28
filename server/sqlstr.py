elements = 'username, password, firstname, surname, email, gender, dob_day, dob_month, dob_year, address1, address2, town, postcode, country, facebook, twitter, instagram, forgot_p_q, forgot_p_a, caption, extrainfo'
sqlstr = ''
for element in elements.split(', '):
	sqlstr += 'userOb[\'' + element + '\'], '
print sqlstr