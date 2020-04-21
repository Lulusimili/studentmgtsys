from flask import Flask, escape, request, render_template
from flask.views import MethodView
import json
import csv

studentCatalog = dict()
moduleCatalog = dict()

with open("moduleCatalog.json", "r") as file:
	moduleCatalog = json.loads(file.read())

with open("studentCatalog.json", "r") as file:
	studentCatalog = json.loads(file.read())

class Student():

	def get_students(self):
		with open("moduleCatalog.json", "r") as file:
			moduleCatalog = json.loads(file.read())

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


class Module(MethodView):

	def add_module(self, moduleID, name, lecturer, capacity):
		self.moduleID = moduleID
		self.name = name
		self.lecturer = lecturer
		self.capacity = capacity

		print('PRINT', moduleID, name, lecturer, capacity)

		moduleCatalog[moduleID] = [name, lecturer, capacity]

		with open("moduleCatalog.json", "r+") as file:
			data = json.load(file)
			data.update(moduleCatalog)
			file.seek(0)
			json.dump(data, file)

	def get(self):
		return "Get"

	def post(self):
		addModuleID = request.form['moduleID']
		addModuleName = request.form['moduleName']
		addModuleLecturer = request.form['moduleLecturer']
		addModuleCapacity = request.form['moduleCapacity']

		self.add_module(addModuleID, addModuleName, addModuleLecturer, addModuleCapacity)

		return render_template('index.html', moduleCatalog=moduleCatalog, studentCatalog=studentCatalog)

	def put(self):
		return "Put"

	def delete(self):
		return "Delete"



app = Flask(__name__)
app.add_url_rule('/add_module', view_func=Module.as_view('add_module'))

@app.route('/')
def main():
	return render_template('index.html', moduleCatalog=moduleCatalog, studentCatalog=studentCatalog)

