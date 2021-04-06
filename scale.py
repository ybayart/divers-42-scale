#! /usr/bin/env python3

from utils import *
import json, datetime

user = input('42 login: ')

req_projects = req_42api('/v2/users/{}/projects_users'.format(user))
if (req_projects == False):
	print(red("User not found :("))
	exit(1)
projects = dict()

for project in req_projects:
	date = datetime.datetime.strptime(project['teams'][0]['created_at'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
	projects[yellow(date) + ': ' + blue(project['project']['name'])] = project['project']['id']

try:
	project = print_inquirer("Select a project", sorted(projects, reverse=True))
except TypeError:
	exit(0)
except KeyboardInterrupt:
	exit(0)
try:
	if project in projects:
		project_name = project
		project = projects[project_name]
		print('Fetching correction scale for:', blue(project_name), '-', yellow(project), '\n')
	else:
		print(red('Select a valid project!'))
		exit(1)
except KeyboardInterrupt:
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
	datas = req_42api('/v2/projects/{}/scale_teams'.format(project), size=100, nb_result=-1, number=i)
	if len(datas) == 0:
		print(red("No scale found :("))
		exit(1)
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
