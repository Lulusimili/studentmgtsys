from flask import Flask, escape, request, render_template, jsonify, redirect, url_for
from flask.views import MethodView
import json
import csv
import os
from collections import Counter
from firebase_admin import credentials, firestore, initialize_app

'''
HOW TO USE
	
	Student Management System is flask application for managing student records. It's functionality ranges from
		- Storing Class Modules
		- Register Students
		- Enrolling Students in Classes
		- Add/Edit Students
		- Add/Edit Students
		- All Users can Borrow and Return Book
	
	To run locally, users must install flask by 

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
	- Heroku
	- Firebase
	- Jquery
	- Jinja2
	- Ajax
	- Bootstrap
	- Javascript
	- HTML/CSS
____________________________________________________'''

studentCatalog = dict()
moduleCatalog = dict()
selectStudentsInModule = dict()
rejectedModules = []

# domainURL = 'https://d19124355studentmgmtsystem.herokuapp.com/'
domainURL = 'http://127.0.0.1:5000/'

# Initialize Firestore DB
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "d19124355-studentmgmtsys-88b1b",
  "private_key_id": "2a35e7fd1d58f702fe659b39d52577cf4481580d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDlrYmKKhZC07sA\nbkJIt++Ezn/sCARq3aUPzGofLEbBZq8J01okMghgXW8L5ZeheQUdoWnpEO02NIrc\nWf25E1F8HS56/ALzmcOSXgfXMv+umbWNpD+Af1gWWRpx/33LG/E/mMxt2xbAX0gz\ndnH8f5wYy180WFeFJmtedlQnSObBaqvK9ci/2SDokU2RdKIEeSv3LPY2C95jHt0b\nr3YWZJeG5hB8yRoavsqAUR4O2FSybCxxI8HsBnzfr3qa3teuIiFYfiR6MkNWlgPc\nU5wZldqPl9AWyrkzggZ2txSoKXmkvtUOcdao3G4CsjkP6mWIw/vIAJKpOVz/lgXt\nHs484ILLAgMBAAECggEAMsKLpzFuAg7xQUMc+x1LnjpVI0ESWNvrYvZ2bbVHXe7n\nuHAxd9Zm64U6yZJQVKt+afIGii/nfRdXqSNqY8DVPWzlnOCddmEBTBPj/7eRsnDe\nIxOtxSRfv3Cp24/vqTfftYJ7i7vj51gniNggkQFS6lfoDpWHojG/gPz91EDUXuJd\nFwiECTB+rGU18J/X9rEJDtZenaERfJLrJ6cRWcwDLJGzDh07oZd9YCBObzNqkecu\nMrKTfTsH6nH+XhonxSWeGjOD0HlS2+LBt9W8P1dlMswSdeHkd5DAiSuloE83HWuW\nO7kR0d3IOMsFpv6nMs7xm1AWZGuWDyodIOHZHyYQ4QKBgQD81GDsms2rfs6/9iSv\nfNGYFF5OP6i+ppcApz49Z89R00Ze0dWOfvONhYskXy6rt9dFYzRboP+JFnkIjUVV\n09mwHkOtOCbO6rKNO5u7cxp7UVHCxW/+JMsxe8Zj0pwBcogpUbT/6UZRmoFF7yc3\n1lq28wWxceRqH1LJ6x/oNtN9nwKBgQDojtaONGCC+Lb87LnF38xYbjw2oehoGlc5\nqTcExhoG+0v+TvedcgbI5iuYRacVaEZs2pgeZVptXJXx8gSVKm5HhLda1lm64vy+\nw++WL4CYHfEe4yD/wDeSj2d8YGPWkVOFpJIuJpn2ZXKD0ATjuGH6xUFD+ScXlzpS\nOZU9P4sTVQKBgQCj5DwsRDE8kUgOsc2YIG5xigqT6LpHVBAgsUksXwXKgg1k29r2\nsx7IR6Ap5LWJRPP8G9HN7/CV+gZdX85pU5oSi5vNRtAJY6R43wIVogixlcZNXtU5\nRrqdCiJRhS3x1j+joT6Wga4+qcxQ/DVNAdvuKl0vaKfrjwCIua0GR7wS+wKBgGVX\ncXoQqwoH9j3rrtzitLrIdubb0VokOGSBL9+dsFPgiHIu2Uq8GObNHqxBlhkHEsF2\n1JlSU4CauyDu9T5Hej0iQYCNLhb5uWgsHCjXVHN1gNCT65pnmg/8+/zASGGFfN8d\nIzKHUcqE1M1KBgdyHwhXkyRa28U0+o5AV5+UJDftAoGBAI415uBpapZmp584ZV6I\nvXa19UmcbebB7oLosGBwdPW4Ek01VeYwV9U2EvtMXZq9LJrdqZ2fowa+xQ8As3H4\nx0Z+D2hRKq+zeMeJHLwXMjZYyx2DPBusIAonLzJmIbEhIUljkT7nYCH30DdqiyGs\nhJUhG4CqZ12a4E5E8ZAr/oRb\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-dw0e5@d19124355-studentmgmtsys-88b1b.iam.gserviceaccount.com",
  "client_id": "113009878211073697270",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-dw0e5%40d19124355-studentmgmtsys-88b1b.iam.gserviceaccount.com"
})


default_app = initialize_app(cred)
db = firestore.client()

studentCatalog_ref = db.collection('studentCatalog')
moduleCatalog_ref = db.collection('moduleCatalog')


# Jinja2 Initialise

def getStudents():
	for key in studentCatalog_ref.stream():
		studentCatalog[key.id] = [key.to_dict()['name'], key.to_dict()['email'], key.to_dict()['modules']]

def getModules():
	for key in moduleCatalog_ref.stream():
		moduleCatalog[key.id] = [key.to_dict()['title'], key.to_dict()['lecturer'], key.to_dict()['capacity']]

getStudents()
getModules()
print(studentCatalog)
class Student(MethodView):
	# Get all students enrolled in a selected module. These students are temporarily added to a dictionary and returned back to javascript for it to be displayed to the user. The dictionary is destroyed once user has changed their module selection.
	def get_student(self, value):

		selectStudentsInModule.clear()
		for key in studentCatalog:
			for module in studentCatalog[key][-1]:
				if module == value:
					selectStudentsInModule[key] = studentCatalog[key][0], studentCatalog[key][1], studentCatalog[key][-1]
		
		return print(selectStudentsInModule)

	# To add a student, users must enter a unique student ID, name and email address. Users also have the option of selecting which modules a student will be enrolled in. This is limited to 5 modules.

	# Each module capacity is checked and ensures no student can be added to a module that may be full. Any module that has reached full capacity is added to a rejected module array and returned back to the user. Any module that has available space is allowed to proceed in the enrollment process.
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

					add_student_info = {'name': str(self.name), 'email':  str(self.email), 'modules':  mlist}
					studentCatalog_ref.document(self.studentID).set(add_student_info)
				else: 
					print(modules, ' is Full')
					rejectedModules.append(modules)
		else:
			studentCatalog[self.studentID] = [str(self.name), str(self.email), self.modulesArray]
			add_student_info = {'name': self.name, 'email':  self.email, 'modules':  self.modulesArray}
			studentCatalog_ref.document(self.studentID).set(add_student_info)

		print(rejectedModules, 'rejectedModules')
		

		return rejectedModules

# SEARCHING A Student

	# The Search feature is build to suport a variety of searches. It recursively searches each student to find match. If search value is not an Student ID, it will search across the columns to find a match. If not match is found, it will continue onto next student, and repeat. The search does not support upper and lower case matching but I hope to implement this in the future.

	def search_student(self, value):
		fetchedStudentResults = dict()
		for key in studentCatalog:
			print(key)
			index = 0
			if value.upper() == key.upper():
				fetchedStudentResults[key] = [studentCatalog[key][0], studentCatalog[key][1], studentCatalog[key][-1]]
			else:
				while index < len(studentCatalog[key]) - 1:
					if value.upper() in studentCatalog[key][index].upper():
						fetchedStudentResults[key] = [studentCatalog[key][0], studentCatalog[key][1]]
						index += 1
					else:
						index += 1

		print(fetchedStudentResults)

		return fetchedStudentResults

	# Students can be removed from module by selecting Module > Selecting Student > Remove. 
	# User must ensure a module has been selected before attempting to remove a user. Once user is removed, the json file is updated.

	def remove_student_from_module(self, studentID, moduleID):

		for module in studentCatalog[studentID][-1]:
			if module == moduleID:
				print(studentCatalog[studentID][-1][0])
				studentCatalog[studentID][-1].pop(0)
		
		return 'removed'

	# Students can be deleted in Students > Select Student > Edit Student > Delete.

	def delete_student(self, key):
		studentCatalog_ref.document(key).delete()
		getStudents()
		return "Student Deleted"


# Post Handling

	# All post handling in doing using a post method and routed to suitable methods. Primarily Ajax was used to post to flask. Any data returned is also handled by jquery and displayed to user.

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
			self.add_student(studentID, studentName, studentEmail, studentModuleList)
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


# All module handling is done using a Module class.

class Module(MethodView):

	# Users can add a module which is then written to a json file, stored locally.
	def add_module(self, moduleID, name, lecturer, capacity):
		self.moduleID = moduleID
		self.name = name
		self.lecturer = lecturer
		self.capacity = capacity

		print('PRINT', moduleID, name, lecturer, capacity)

		add_module_info = {'title': str(self.name), 'lecturer':  str(self.lecturer), 'capacity':  self.capacity}
		moduleCatalog_ref.document(str(self.moduleID)).set(add_module_info)

		return redirect(domainURL, code=302)

	# Users can delete a module. Once a module is delete, all instances of that module is removed from a students enrollment history.
	def delete_module(self, key):
		moduleCatalog_ref.document(key).delete()


	# Users can edit any module.

	def edit_module(self, moduleID, name, lecturer, capacity):
		self.moduleID = moduleID
		self.name = name
		self.lecturer = lecturer
		self.capacity = capacity

		moduleCatalog[moduleID][0] = name
		moduleCatalog[moduleID][1] = lecturer
		moduleCatalog[moduleID][2] = int(capacity)

		edit_module_info = {'title': self.name, 'lecturer':  self.lecturer, 'capacity':  self.capacity}
		moduleCatalog_ref.document(self.moduleID).set(edit_module_info)


	# Searching a module is similar to searching a student, and support a variety of different search words.
	def search_module(self, value):
		fetchModulesResults = dict()
		for key in moduleCatalog:
			index = 0
			print(key)
			if value.upper() == key.upper():
				print(value.upper(), key.upper())
				fetchModulesResults[key] = [moduleCatalog[key][0], moduleCatalog[key][1], moduleCatalog[key][2]]
			else:
				while index < len(moduleCatalog[key]) - 1:
					if value.upper() in moduleCatalog[key][index].upper():
						fetchModulesResults[key] = [moduleCatalog[key][0], moduleCatalog[key][1]]
						index += 1
					else:
						index += 1

		print(fetchModulesResults)

		return fetchModulesResults

# Post Handling

	# All post handling in doing using a post method and routed to suitable methods. Primarily Ajax was used to post to flask. Any data returned is also handled by jquery and displayed to user.

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
	getStudents()
	getModules()
	moduleList = []
	for student in studentCatalog:
		for module in studentCatalog[student][-1]:
			moduleList.append(module)
	enrollmentFigures = (Counter(moduleList))

	# Returns index.html along with dictionarys for jinja2 to display in html format.

	return render_template('index.html', moduleCatalog=moduleCatalog, studentCatalog=studentCatalog, selectStudentsInModule=selectStudentsInModule, rejectedModules=rejectedModules, enrollmentFigures=enrollmentFigures)

if __name__ == '__main__':
	TEMPLATES_AUTO_RELOAD = True
	app.run()