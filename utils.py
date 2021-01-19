import requests, time, os

# COLORS
def red(str): return "\033[91m{}\033[0m".format(str)
def green(str): return "\033[92m{}\033[0m".format(str)
def yellow(str): return "\033[93m{}\033[0m".format(str)
def blue(str): return "\033[94m{}\033[0m".format(str)
def pink(str): return "\033[95m{}\033[0m".format(str)

url = "https://api.intra.42.fr"
errors = []
client = os.environ.get('API42_CLIENT')
if client == None:
	errors.append("env API42_CLIENT not set :(")
secret = os.environ.get('API42_SECRET')
if secret == None:
	errors.append("env API42_SECRET not set :(")
if len(errors) > 0:
	for error in errors:
		print(red(error))
	exit(1)

access_token = requests.post("{}/oauth/token?grant_type=client_credentials&client_id={}&client_secret={}".format(url, client, secret)).json()["access_token"]

def req_42api(path, payload=dict(), size=100, nb_result=0, number=1):
	global access_token
	loop = 1
	datas = []
	internal_payload = {
		'page':
		{
			'number': number,
			'size': size
		}
	}
	calc_payload = {**payload, **internal_payload}
	while loop == 1:
		req = requests.get(url+path, json=calc_payload, headers={"Authorization": "Bearer "+access_token})
		if req.status_code == 429:
			if float(req.headers['Retry-After']) > 10:
				print('Waiting {}s'.format(req.headers['Retry-After']))
			time.sleep(float(req.headers["Retry-After"]))
		elif req.status_code == 200:
			datas += req.json()
			if (nb_result == -1 or
				int(req.headers["X-Page"]) * int(req.headers["X-Per-Page"]) >= int(req.headers["X-Total"]) or
				(nb_result > 0 and int(req.headers["X-Page"]) * int(req.headers["X-Per-Page"]) >= nb_result)):
				loop = 0
			calc_payload['page']['number'] += 1
		elif req.status_code == 401:
			access_token = requests.post("{}/oauth/token?grant_type=client_credentials&client_id={}&client_secret={}".format(url, client, secret)).json()["access_token"]
		elif req.status_code == 404:
			return False
	return datas
