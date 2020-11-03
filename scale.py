#! /usr/bin/python3

from utils import *

user = input('42 login: ')

req_projects = req_42api('/v2/users/{}/projects_users'.format(user))
projects = dict()

for project in req_projects:
	projects[project['project']['name']] = project['project']['id']

for project in sorted(projects):
	print("{}: {}".format(yellow(project), blue(projects[project])))

try:
	project = int(input('?> '))
except:
	print('This is not a valid number')
	exit(1)

payload = {
	'filter':
	{
		'filled': 'true'
	}
}
datas = req_42api('/v2/projects/{}/scale_teams'.format(project), payload=payload, size=1, nb_result=1)

for data in datas:
	questions = dict()
	for question in data["questions_with_answers"]:
		questions[question["id"]] = {
			"name": question["name"],
			"guide": question["guidelines"]
		}
	for question in sorted(questions):
		print(questions[question]["name"])
		print(questions[question]["guide"])
		print("")
