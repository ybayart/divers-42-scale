#! /usr/bin/env python3

from utils import *
import json

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
i = 1
loop = True
while loop:
	datas = req_42api('/v2/projects/{}/scale_teams'.format(project), payload=payload, size=100, nb_result=i)
	for data in datas:
		if data["questions_with_answers"]:
			loop = False
			break
	i += 1

rating = {
	'bool': "[ {} | {} ]".format(green('Yes'), red('No')),
	'multi': "[{0}--{0}--{0}--{0}--{0}--{0}]".format(pink('#'))
}
questions = dict()
for question in data["questions_with_answers"]:
	questions[question["id"]] = {
		"name": question["name"],
		"guide": question["guidelines"],
		"rating": question["rating"]
	}
for question in sorted(questions):
	print(yellow(questions[question]["name"]), rating[questions[question]["rating"]])
	print(blue(questions[question]["guide"]))
	print("")
