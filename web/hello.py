def application(environ, start_responce):	
	status = '200 OK'
	headers = [
		('Content-Type', 'text/plain')
	]
	queryString = environ['QUERY_STRING'].replace('&','\n')
	start_responce(status, headers)
	return queryString
