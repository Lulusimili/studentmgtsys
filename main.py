from flask import Flask, escape, request, render_template, jsonify, redirect
from flask.views import MethodView
import json
import csv

domainURL = 'http://127.0.0.1:5000/'

studentCatalog = dict()
moduleCatalog = dict()

editModuleKey = 'HELLO'

with open("moduleCatalog.json", "r") as file:
	moduleCatalog = json.loads(file.read())

with open("studentCatalog.json", "r") as file:
	studentCatalog = json.loads(file.read())

class Student(MethodView):

	def get_students(self):
		with open("moduleCatalog.json", "r") as file:
			moduleCatalog = json.loads(file.read())

	def fetch_module_students(self):
		print('received')

	def add_student(self, studentID, name, email):
		self.studentID = studentID
		self.name = name
		self.email = email

		studentCatalog[self.studentID] = [self.name, self.email]

		with open("studentCatalog.json", "r+") as file:
			data = json.load(file)
			data.update(studentCatalog)
			file.seek(0)
			json.dump(data, file)


	def post(self):
		selectedModule = request.get_data()
		print(str(selectedModule))
		return "Post"

	def get(self):
		return "Get THIS IS A GET"

	def put(self):
		return "Put"

	def delete(self):
		return "Delete"


class Module(MethodView):

	def add_module(self, moduleID, name, lecturer, capacity):
		self.moduleID = moduleID
		self.name = name
		self.lecturer = lecturer
		self.capacity = capacity

		print('PRINT', moduleID, name, lecturer, capacity)

		moduleCatalog[str(moduleID)] = [name, lecturer, capacity]

		with open("moduleCatalog.json", "r+") as file:
			data = json.load(file)
			data.update(moduleCatalog)
			file.seek(0)
			json.dump(data, file)

		return redirect(domainURL, code=302)

	def delete_module(self, key):
		moduleCatalog.pop(str(key), None)	

		with open('moduleCatalog.json', 'w') as updatedModuleJSON:
			json.dump(moduleCatalog, updatedModuleJSON)

	def edit_module(self, key):
		global editModuleKey 
		editModuleKey = key

		return editModuleKey

	def get(self):

		return "GET"

	def post(self):

		if (request.url == (domainURL +'module-edit')):
			data = request.get_json()
			return self.edit_module(data['id'])
		
		if (request.url == (domainURL +'module-remove')):
			data = request.get_json()
			self.delete_module(data['id'])


		if (request.url == (domainURL + 'add_module')):
			addModuleID = request.form['moduleID']
			addModuleName = request.form['moduleName']
			addModuleLecturer = request.form['moduleLecturer']
			addModuleCapacity = request.form['moduleCapacity']

			print(addModuleID, addModuleName, addModuleLecturer, addModuleCapacity)

			self.add_module(addModuleID, addModuleName, addModuleLecturer, addModuleCapacity)

		return redirect(domainURL, code=302)

	def put(self):
		return "Put"

	def delete(self):
		return "Delete"



app = Flask(__name__)
app.add_url_rule('/add_module', view_func=Module.as_view('add_module'))
app.add_url_rule('/module-remove', view_func=Module.as_view('delete_module'))
app.add_url_rule('/module-edit', view_func=Module.as_view('edit_module'))
app.add_url_rule('/module-selected', view_func=Student.as_view('fetch_module_students'))


@app.route('/')
def main():
	return render_template('index.html', moduleCatalog=moduleCatalog, studentCatalog=studentCatalog, editModuleKey=editModuleKey)

