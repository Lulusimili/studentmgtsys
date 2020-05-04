from flask import Flask, escape, request, render_template, jsonify, redirect, url_for
from flask.views import MethodView
import json
import csv
from collections import Counter

domainURL = 'http://127.0.0.1:5000/'

studentCatalog = dict()
moduleCatalog = dict()
selectStudentsInModule = dict()
rejectedModules = []
fetchedModuleResults = dict()

global initialModuleID

'''
HOW TO USE
	
	Student Management System is flask application for managing student records. It's functionality ranges from
		- Storing Class Modules
		- Register Students
		- Enrolling Students in Classes
		- Add/Edit Students
		- Add/Edit Students
		- All Users can Borrow and Return Book
	
	Prior to using, users must install flask by 

		pip install flask

	Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.
	Documentation can be found here - https://pypi.org/project/Flask/

	Once Flask is installed, the application can be run by typing the following into the terminal in the directory of main.py:
	
		- export FLASK_APP=main.py
		- flask run
		- Open http://127.0.0.1:5000/ in browser.

TECHNOLOGIES USED

	- Python
	- Flask
	- Jquery
	- Ajax
	- Bootstrap
	- Javascript
	- HTML/CSS
____________________________________________________'''

with open("moduleCatalog.json", "r") as file:
	moduleCatalog = json.loads(file.read())

with open("studentCatalog.json", "r") as file:
	studentCatalog = json.loads(file.read())


class Student(MethodView):
	# Get all students enrolled in a selected module. These students are temporarily added to a dictionary and returned back to javascript for it to be displayed to the user. The dictionary is destroyed once user has changed their module selection.
	def get_student(self, value):

		selectStudentsInModule.clear()
		for key in studentCatalog:
			for module in studentCatalog[key][-1]:
				if module == value:
					selectStudentsInModule[key] = studentCatalog[key][0], studentCatalog[key][1], studentCatalog[key][-1]

		with open("moduleCatalog.json", "r") as file:
			moduleCatalog = json.loads(file.read())
		
		return print(selectStudentsInModule)

	# Add students
	def add_student(self, studentID, name, email, modulesArray):
		self.studentID = studentID
		self.name = name
		self.email = email
		self.modulesArray = modulesArray
		rejectedModules.clear()
		# Find Capacity of Selected Modules
		mlist = []

		if (len(self.modulesArray) > 0):
			for modules in self.modulesArray:
				moduleCapacity = moduleCatalog[modules][2]
				moduleCounter = 0
				
				# Find Current Number of Students enrolled in Module
				for students in studentCatalog:
					for studentModules in studentCatalog[students][-1]:
						if (studentModules == modules or len(modules) == 0):
							moduleCounter += 1
				print(moduleCounter, 'Students in ', modules)

				# Ensures no student can ensure in a module that is full.
				if (len(self.modulesArray) <= 5 and moduleCounter < int(moduleCapacity)):

					mlist.append(modules)
					studentCatalog[self.studentID] = [self.name, self.email, mlist]
				else: 
					print(modules, ' is Full')
					rejectedModules.append(modules)
		else:
			studentCatalog[self.studentID] = [self.name, self.email, self.modulesArray]

		print(rejectedModules, 'rejectedModules')
		
		with open("studentCatalog.json", "w") as file:
					json.dump(studentCatalog, file, indent=2)

		return rejectedModules


# Edit Student

	# Students can be edited in the Student Section > Edit Student.

	# User must ensure that a student is selected before edit button is enabled.

	# Students can be removed or added to modules through the edit student modal.


	def edit_student(self, studentID, name, email, modulesArray):
		self.studentID = studentID
		self.name = name
		self.email = email
		self.modulesArray = modulesArray
		rejectedModules.clear()
		# Find Capacity of Selected Modules
		mlist = []


		if (len(self.modulesArray) > 0):
			for modules in self.modulesArray:
				moduleCapacity = moduleCatalog[modules][2]
				moduleCounter = 0
				
				# Find Current Number of Students enrolled in Module
				for students in studentCatalog:
					for studentModules in studentCatalog[students][-1]:
						if (studentModules == modules or len(modules) == 0):
							moduleCounter += 1
				print(moduleCounter, 'Students in ', modules)
				# Ensures no student can ensure in a module that is full.
				if (len(self.modulesArray) <= 5 and moduleCounter < int(moduleCapacity)):

					mlist.append(modules)
					studentCatalog[self.studentID] = [self.name, self.email, mlist]
				else: 
					print(modules, ' is Full')
					rejectedModules.append(modules)
		else:
			studentCatalog[self.studentID] = [self.name, self.email, self.modulesArray]

		print(rejectedModules, 'rejectedModules')
		
		with open("studentCatalog.json", "w") as file:
					json.dump(studentCatalog, file, indent=2)

		return rejectedModules


# SEARCHING A Student

	# The Search feature is build to suport a variety of searches. It recursively searches each student to find match. If search value is not an Student ID, it will search across the columns to find a match. If not match is found, it will continue onto next student, and repeat.

	def search_student(self, value):
		fetchedStudentResults = dict()
		fetchCounter = 0
		for key in studentCatalog:
			index = 0
			if value == key:
				fetchedStudentResults[key] = [studentCatalog[key][0], studentCatalog[key][1], studentCatalog[key][2]]
			else:
				while index < len(studentCatalog[key]) - 1:
					if value in studentCatalog[key][index]:
						fetchedStudentResults[key] = [studentCatalog[key][0], studentCatalog[key][1], studentCatalog[key][2]]
						index += 1
					else:
						index += 1

		print(fetchedStudentResults)

		return fetchedStudentResults

	def remove_student_from_module(self, studentID, moduleID):

		for module in studentCatalog[studentID][-1]:
			if module == moduleID:
				print(studentCatalog[studentID][-1][0])
				studentCatalog[studentID][-1].pop(0)
		
		with open('studentCatalog.json', 'w') as updatedStudentJSON:
			json.dump(studentCatalog, updatedStudentJSON)
		return 'removed'

	def delete_student(self, key):
		studentCatalog.pop(str(key), None)
		print(studentCatalog)	

		with open('studentCatalog.json', 'w') as updatedStudentJSON:
			json.dump(studentCatalog, updatedStudentJSON)

		return "Student Deleted"


# Post Handling

	# All post handling in doing using a post method. Primarily Ajax was used to post to flask.

	def post(self):

		if (request.url == (domainURL + 'delete-student')):
			data = request.get_json()
			print(data['id'])
			if (len(data) > 0):
				return self.delete_student(data['id'])

		if (request.url == (domainURL + 'search-students')):
			data = request.form['search']
			print(data)
			if (len(data) > 0):
				return self.search_student(data)


		if (request.url == (domainURL + 'remove-student-from-module')):
			data = request.get_json()
			print(data)
			studentID = data['studentID']
			moduleID = data['moduleID']

			self.remove_student_from_module(studentID, moduleID)
			return 'removed'

		if (request.url == (domainURL + 'edit-student')):
			studentID = request.form['studentID']
			studentName = request.form['studentName']
			studentEmail = request.form['studentEmail']
			studentModuleList = request.form.getlist('moduleEnrollment')
			print(studentID, studentName, studentEmail, studentModuleList, 'from edit form')
			self.edit_student(studentID, studentName, studentEmail, studentModuleList)
			return jsonify(rejectedModules)

		if (request.url == (domainURL + 'select-edit-students')):
			data = request.get_json()

			selectedStudentID = data['id']
			return jsonify(studentCatalog[data['id']])

		if (request.url == (domainURL + 'get-all-students')):
			return jsonify(studentCatalog)

		if (request.url == (domainURL + 'get-selected-students')):
			data = request.json
			self.get_student(data['id'])
			return redirect(domainURL, code=302)

		if (request.url == (domainURL + 'register-student')):
			status = {}
			studentID = request.form['studentID']
			studentName = request.form['studentName']
			studentEmail = request.form['studentEmail']
			studentEnrollment = request.form.getlist('moduleEnrollment')

			print(studentID, studentName, studentEmail, studentEnrollment)

			if studentID not in studentCatalog:
			    self.add_student(studentID, studentName, studentEmail, studentEnrollment)
			else:
				status = {'status': 'AlreadyExists'}
				print(status)
				return status

		return jsonify(status)

		return "Post"

	def get(self):
		print('get')
		return 'hello get'

class Module(MethodView):

	def add_module(self, moduleID, name, lecturer, capacity):
		self.moduleID = moduleID
		self.name = name
		self.lecturer = lecturer
		self.capacity = capacity

		print('PRINT', moduleID, name, lecturer, capacity)

		moduleCatalog[str(moduleID)] = [name, lecturer, capacity]

		with open("moduleCatalog.json", "w") as file:
			json.dump(moduleCatalog, file, indent=2)

		return redirect(domainURL, code=302)

	def delete_module(self, key):
		for student in studentCatalog:
			for module in studentCatalog[student][-1]:
				if module == key:
					print(studentCatalog[student][-1][0])
					studentCatalog[student][-1].pop(0)

		moduleCatalog.pop(str(key), None)

		with open('moduleCatalog.json', 'w') as updatedModuleJSON:
			json.dump(moduleCatalog, updatedModuleJSON)

	def edit_module(self, moduleID, name, lecturer, capacity):

		moduleCatalog[moduleID][0] = name
		moduleCatalog[moduleID][1] = lecturer
		moduleCatalog[moduleID][2] = int(capacity)

		with open("moduleCatalog.json", "w") as file:
			json.dump(moduleCatalog, file, indent=2)
			print('Module {} edited.'.format(moduleID))

	def search_module(self, value):
		fetchedModuleResults.clear()
		fetchCounter = 0
		for key in moduleCatalog:
			index = 0
			if value == key:
				fetchedModuleResults[key] = [moduleCatalog[key][0], moduleCatalog[key][1]]
			else:
				while index < len(moduleCatalog[key]) - 3:
					if value in moduleCatalog[key][index]:
						fetchedModuleResults[key] = [moduleCatalog[key][0], moduleCatalog[key][1]]
						index += 1
					else:
						index += 1

		print(fetchedModuleResults)

		return fetchedModuleResults


	def post(self):
		print(request.url)

		if (request.url == (domainURL + 'search-modules')):
			data = request.form['search']
			print(data)

			if (len(data) > 0):
				return self.search_module(data)

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

		return "Post"


# Routing
	# Below all routing is handled and sent to appropriate methods.

app = Flask(__name__, template_folder='templates')
app.add_url_rule('/add_module', view_func=Module.as_view('add_module'))
app.add_url_rule('/module-remove', view_func=Module.as_view('delete_module'))
app.add_url_rule('/module_edit', view_func=Module.as_view('edit_module'))
app.add_url_rule('/select-module-edit', view_func=Module.as_view('edit_module2'))
app.add_url_rule('/get-selected-students', view_func=Student.as_view('get_student'))
app.add_url_rule('/register-student', view_func=Student.as_view('add_student'))
app.add_url_rule('/remove-student', view_func=Student.as_view('remove_student'))
app.add_url_rule('/edit-student', view_func=Student.as_view('edit_student'))
app.add_url_rule('/select-edit-students', view_func=Student.as_view('get_selected_student'))
app.add_url_rule('/remove-student-from-module', view_func=Student.as_view('remove-student-from-module'))
app.add_url_rule('/search-students', view_func=Student.as_view('search_student'))
app.add_url_rule('/search-modules', view_func=Module.as_view('search_module'))
app.add_url_rule('/delete-student', view_func=Student.as_view('delete_student'))

@app.route('/')
def main():
	moduleList = []
	for student in studentCatalog:
		for module in studentCatalog[student][-1]:
			moduleList.append(module)
	enrollmentFigures = (Counter(moduleList))

	return render_template('index.html', moduleCatalog=moduleCatalog, studentCatalog=studentCatalog, selectStudentsInModule=selectStudentsInModule, rejectedModules=rejectedModules, enrollmentFigures=enrollmentFigures)

if __name__ == '__main__':
	TEMPLATES_AUTO_RELOAD = True
	app.run()