from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "Secret Key"


# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:3306/ta_listing"
# app.config['SQLALCHEMY_DATABASE_URI'] =  "mysql://b6f4c2bb784eb6:a6d604a2@us-cdbr-east-02.cleardb.com/heroku_bb881c2fc78bb76?reconnect=true"



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)
CORS(app)

class Modules(db.Model):

    __tablename__ = 'modules'
    mod_id = db.Column(db.Integer, primary_key = True, nullable=False)
    mod_name = db.Column(db.String(30), nullable=False)
    positions_available = db.Column(db.Integer, nullable=False)
    job_scope = db.Column(db.String(99), nullable=False)
    professor_name = db.Column(db.String(30), nullable=False)
    professor_id = db.Column(db.String(12), nullable=False)
    school = db.Column(db.String(1000), nullable=False)
    level = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    numberOfStudents = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(11), nullable=False)
    start_date = db.Column(db.DateTime(), nullable = False)
    end_date = db.Column(db.DateTime(), nullable = False)
    rating1 = db.Column(db.Integer, nullable=False)
    rating2 = db.Column(db.Integer, nullable=False)
    rating3 = db.Column(db.Integer, nullable=False)
    rating4 = db.Column(db.Integer, nullable=False)
    rating5 = db.Column(db.Integer, nullable=False)




    def __init__(self, mod_id, mod_name, positions_available , job_scope ,professor_name, 
    professor_id, school, level, description, numberOfStudents, location, start_date, end_date, rating1,rating2, rating3, rating4, rating5):

        self.mod_id = mod_id
        self.mod_name = mod_name
        self.positions_available = positions_available
        self.job_scope = job_scope
        self.professor_name = professor_name
        self.professor_id = professor_id
        self.school = school
        self.level = level
        self.description = description
        self.numberOfStudents = numberOfStudents
        self.location = location
        self.start_date = start_date 
        self.end_date = end_date
        self.rating1 = rating1
        self.rating2 = rating2
        self.rating3 = rating3
        self.rating4= rating4
        self.rating5 = rating5


    def json(self):
        return {
            "mod_id": self.mod_id , "mod_name": self.mod_name, 
            "positions_available": self.positions_available, "job_scope": self.job_scope, 
            "professor_name": self.professor_name, "professor_id": self.professor_id, "school":self.school, "level":self.level,
            "description": self.description, "numberOfStudents": self.numberOfStudents, "location": self.location, "start_date": self.start_date,"end_date": self.end_date,
            "rating1":self.rating1,"rating2":self.rating2,"rating3":self.rating3,"rating4":self.rating4,"rating5":self.rating5
        }

@app.route('/get_all')
def get_all():
	return jsonify({"modules": [module.json() for module in Modules.query.all()]})

@app.route('/add_course/<string:course>')
def add_course(course):
    module = []
    course = course.split("&")
    for param in course:
        temp = param.split("=")
        module.append(temp[1])

    try:
        me = Modules(module[0], module[1], module[2], module[3], module[4], module[5], module[6], module[7], module[8], 234, 'SIS SR 2-3', '2020-08-17','2020-11-29', 0, 0, 0, 0, 0)
        db.session.add(me)
        db.session.commit()
        return jsonify("Module added")
    except:
        return jsonify("Module exists")


@app.route('/update_rating/<string:details>')
def update_rating(details):

    rating_details = []
    details = details.split("&")

    
    for param in details:
        temp = param.split("=")
        rating_details.append(temp[1])

    module = Modules.query.filter_by(mod_id=rating_details[0]).first()

    print(module)

    module.rating1 += int(rating_details[1])
    module.rating2 += int(rating_details[2])
    module.rating3 += int(rating_details[3])
    module.rating4 += int(rating_details[4])
    module.rating5 += int(rating_details[5])


    try:
        db.session.commit()
        return jsonify("Rating updated")
    except:
        return jsonify("Invalid Module")



# ! port numbers
# account = 5010
# applications = 5011
# modules = 5012
# payments = 5013
# professors = 5014
# students = 5015
# student_experience = 5016
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True)
