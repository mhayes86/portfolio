# Do not name python file flask.py since it will conflict with flask package

from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)  # __name__ is name of app, or in this case, __main__

# Root web page
@app.route('/')
def my_home_root():
	return render_template("index.html")

# Each web page uses its name as the URL so a new function isnt' needed
# for each page
@app.route('/<string:page_name>')
def html_page(page_name):
	return render_template(page_name)


# Imitate writing data to a database by writing it to a file from the 
# contact.html page
def write_to_file(data):
	with open('database.txt', mode="a") as database:
		email = data["email"]
		subject = data["subject"]
		message = data["message"]
		file = database.write(f"\n{email},{subject},{message}")	

# Saem as write_to_file, but writes to csv instead
# Be sure to import csv module
def write_to_csv(data):
	with open("database.csv", mode="a", newline="") as database_csv:
		email = data["email"]
		subject = data["subject"]
		message = data["message"]
		csv_writer = csv.writer(database_csv, 
								delimiter=",", 
								quotechar='"', 
								quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow([email,subject,message])


# Adds POST request method on for the form element in contact.html
# The contact.html was given names to each form part (email, subject, message)
# and if that form gets a POST, those become variables in this python script that
# can be used, such as in the write to file above.
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
    	try:
	        data = request.form.to_dict()
	        # print(data) # This just prints that the data was posted in terminal
	        # Calls the write_to_file function above to write the data to a file
	        # write_to_file(data)
	        write_to_csv(data)
	        return redirect("/thank_you.html")
	    except:
	    	return "Did not save to database."
    else:
        return "Something went wrong. Request method was not POST."