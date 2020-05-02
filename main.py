from flask import Flask, escape, request, render_template, jsonify, redirect
from flask.views import MethodView
import json
import csv

domainURL = 'http://127.0.0.1:5000/'

studentCatalog = dict()
moduleCatalog = dict()

global initialModuleID

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
		return "Get"

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

	def edit_module(self, moduleID, name, lecturer, capacity):

		moduleCatalog[moduleID][0] = name
		moduleCatalog[moduleID][1] = lecturer
		moduleCatalog[moduleID][2] = int(capacity)

		with open("moduleCatalog.json", "w") as file:
			json.dump(moduleCatalog, file)
			print('Module {} edited.'.format(moduleID))


	def get(self):

		return "Get"

	def post(self):
		print(request.url)

		# Get Selected Modules Key/ID to query Dictionary
		if (request.url == (domainURL +'select-module-edit')):
			data = request.get_json()

			initialModuleID = data['id']
			return jsonify(moduleCatalog[data['id']])

		# Get edited module information based on user input
		elif (request.url == 'http://127.0.0.1:5000/module_edit'):
			editModuleID = request.form['moduleID']
			editModuleName = request.form['moduleName']
			editModuleLecturer = request.form['moduleLecturer']
			editModuleCapacity = request.form['moduleCapacity']
			self.edit_module(editModuleID, editModuleName, editModuleLecturer, editModuleCapacity)
			return redirect(domainURL, code=302)


		
		# Get delete request and send to send delete method
		elif (request.url == (domainURL + 'module-remove')):
			data = request.get_json()
			self.delete_module(data['id'])
			return redirect(domainURL, code=302)

		# Get add module request and send to send add module method
		# New Module information based on User Input
		elif (request.url == (domainURL + 'add_module')):
			addModuleID = request.form['moduleID']
			addModuleName = request.form['moduleName']
			addModuleLecturer = request.form['moduleLecturer']
			addModuleCapacity = request.form['moduleCapacity']

			print(addModuleID, addModuleName, addModuleLecturer, addModuleCapacity)

			self.add_module(addModuleID, addModuleName, addModuleLecturer, addModuleCapacity)

			return redirect(domainURL, code=302)

		else:
			return redirect(domainURL, code=302)

		return "postposty"

	def put(self):
		return "Put"

	def delete(self):
		return "Delete"


app = Flask(__name__)
app.add_url_rule('/add_module', view_func=Module.as_view('add_module'))
app.add_url_rule('/module-remove', view_func=Module.as_view('delete_module'))
app.add_url_rule('/module_edit', view_func=Module.as_view('edit_module'))
app.add_url_rule('/select-module-edit', view_func=Module.as_view('edit_module2'))
app.add_url_rule('/module-selected', view_func=Student.as_view('fetch_module_students'))


@app.route('/')
def main():
	return render_template('index.html', moduleCatalog=moduleCatalog, studentCatalog=studentCatalog)

if __name__ == '__main__':
    app.run()