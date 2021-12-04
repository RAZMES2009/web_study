from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dance_teacher.db'

db = SQLAlchemy(app)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    second_name = db.Column(db.String(10), nullable=True)
    type_dance = db.Column(db.String(20), nullable=True)

class Time_teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_day = db.Column(db.String, nullable=True)
    date_h = db.Column(db.Text)
    teacher_id = db.Column(db.Integer)
    day_id = db.Column(db.Integer)
    
class Style_dance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_dance = db.Column(db.Text)
    description = db.Column(db.Text)
        

@app.route('/style')
@app.route('/')
def main():
    style_dance = Style_dance.query.all()
    return render_template('styl.html', style=style_dance)

@app.route('/schedule')
def schedule():
    teacher = Teacher.query.all()
    time_teacher = Time_teacher.query.all()
    
    if teacher:
        return render_template('schedule.html', time_teacher=time_teacher, dance_teacher=teacher)
    else:
        return "Извините, но пока ближайших занятий нет"

@app.route('/about-style/<id>')
def about_style(id):
    id = int(id) - 1
    style_dance = Style_dance.query.all()
    return render_template('about-style.html', style=style_dance, i=id)

@app.route('/abon')
def abon():
    return render_template('abon.html')

@app.route('/create_rasp', methods=['POST', 'GET'])
def create_rasp():
    if request.method == 'POST':
        name = request.form['name']
        second_name = request.form['second_name']
        date_day = request.form['date_day']
        date_h = request.form['date_h']
        type_dance = request.form['type_dance']
        day_id = None
        teacher_id = None
        q = db.session.query(Teacher.id)
        if db.session.query(q.exists()).scalar():
            for id in db.session.query(Teacher.id).distinct():
                teacher_id = id[-1] + 1
        else:
            teacher_id = 1

        if date_day == 'Понедельник': day_id = 1
        elif date_day == 'Вторник': day_id = 2
        elif date_day == 'Среда': day_id = 3
        elif date_day == 'Четверг': day_id = 4
        elif date_day == 'Пятница': day_id = 5

        teacher = Teacher(name=name, second_name=second_name, type_dance=type_dance)
        time_teacher = Time_teacher(date_day=date_day, date_h=date_h, day_id=day_id, teacher_id=teacher_id)
        try:
            db.session.add(teacher)
            db.session.add(time_teacher)
            db.session.commit()
            return redirect('/create_rasp')
        except:
            return "Ошибка"
    else:
        return render_template('create_rasp.html')
    
@app.route('/create-style', methods=['POST', 'GET'])
def create_style():
    if request.method == 'POST':
        name_dance = request.form['name_style']
        description = request.form['description_style']
        
        style_dance = Style_dance(name_dance=name_dance, description=description)
        
        try:
            db.session.add(style_dance)
            db.session.commit()
            return redirect('/create-style')
        except:
            return "Ошибка"
    else:
        return render_template('create-style.html')
    
@app.route('/del/<id>')
def delete(id):
    try:
        db.session.query(Teacher).filter(Teacher.id==id).delete()
        db.session.query(Time_teacher).filter(Time_teacher.teacher_id==id).delete()
        
        q = db.session.query(Teacher.id)
        if db.session.query(q.exists()).scalar():
            f_teacher = Teacher.query.first()
            f_time = Time_teacher.query.first()
            if f_teacher.id != 1:
                f_teacher.id = id
                f_time.teacher_id = id

        db.session.commit()
        return redirect('/schedule')    
    except:
            return "Ошибка"  
        
@app.route('/about-teacher')
def about_teacher():
    teacher = Teacher.query.all()
    return render_template('about-teacher.html', teacher=teacher)  

if __name__ == '__main__':
    app.run()