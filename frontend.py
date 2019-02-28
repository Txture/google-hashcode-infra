from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import os
import math
import uuid
import subprocess
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms_alchemy import model_form_factory
from sqlalchemy_utils import database_exists


app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy(app)

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

"""
model
"""

class Problem(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    inputfile = db.Column(db.Text)

    def __repr__(self):
        return 'Problem {}'.format(self.name)


class Run(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    score = db.Column(db.Integer, index=True)
    parameter_set = db.Column(db.Text)
    problem_id = db.Column(db.String(80))
    result = db.Column(db.Text)

    def __repr__(self):
        return 'Run {}'.format(self.name)

db.create_all()

"""
forms
"""

class ProblemForm(ModelForm):
    name = SelectField('Problem', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')])
    input = TextAreaField('Input')


class RunForm(ModelForm):
    problem = SelectField('Problem', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')])

    param1_start = StringField('param1_start')
    param1_step = StringField('param1_step')
    param1_end = StringField('param1_end')

    param2_start = StringField('param2_start')
    param2_step = StringField('param2_step')
    param2_end = StringField('param2_end')

    param3_start = StringField('param3_start')
    param3_step = StringField('param3_step')
    param3_end = StringField('param3_end')

    param4_start = StringField('param4_start')
    param4_step = StringField('param4_step')
    param4_end = StringField('param4_end')

    param5_start = StringField('param5_start')
    param5_step = StringField('param5_step')
    param5_end = StringField('param5_end')


@app.route('/problem', methods=['GET', 'POST'])
def problem_submit():
    form = ProblemForm()
    if form.validate_on_submit():
        p = Problem.query.filter_by(name=form.name.data).first()
        if p is None:
            p = Problem(name=form.name.data,
                        inputfile=form.input.data)
            db.session.add(p)
        else:
            p.name = form.name.data
            p.inputfile = form.input.data

        db.session.commit()
        return redirect('/')
    return render_template('problem.html', form=form)


@app.route('/result', methods=['GET', 'POST'])
def result():
    score = request.form.get('score')
    problem = request.form.get('problem')
    result = request.form.get('result')
    param1 = request.form.get('param1')
    param2 = request.form.get('param2')
    param3 = request.form.get('param3')
    param4 = request.form.get('param4')
    param5 = request.form.get('param5')

    paramset = 'p1{}p2{}p3{}p4{}p5{}'.format(param1, param2, param3, param4, param5)

    r = Run(score=score,
            result=result,
            parameter_set=paramset,
            problem_id=problem,
            id=str(uuid.uuid4()))

    db.session.add(r)
    db.session.commit()

    return '42'


def combinations(start, end, step):
    if not start or not end or not step:
        return 1
    if step == 0:
        step = 1
    return math.floor((float(end)-float(start))/float(step))


def comb_iterator(start, end, step):
    if not start or not end or not step:
        return None

    current = float(start)
    while current <= float(end):
        yield current
        current += float(step)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = RunForm()
    if form.validate_on_submit():
        comb1 = combinations(form.param1_start.data, form.param1_end.data, form.param1_step.data)
        comb2 = combinations(form.param2_start.data, form.param2_end.data, form.param2_step.data)
        comb3 = combinations(form.param3_start.data, form.param3_end.data, form.param3_step.data)
        comb4 = combinations(form.param4_start.data, form.param4_end.data, form.param4_step.data)
        comb5 = combinations(form.param5_start.data, form.param5_end.data, form.param5_step.data)

        problem = Problem.query.filter_by(name=form.problem.data).get()

        print('{} combinations'.format(comb1*comb2*comb3*comb4*comb5))

        if comb1*comb2*comb3*comb4*comb5 > 100:
            flash('too many options crazy bitch')
            return redirect('/')

        comb_it1 = comb_iterator(form.param1_start.data, form.param1_end.data, form.param1_step.data)
        if comb_it1 is None:
            flash('invalid')
            return redirect('/')

        for param1 in comb_it1:
            comb_it2 = comb_iterator(form.param2_start.data, form.param2_end.data, form.param2_step.data)
            if comb_it2 is None:
                # only start for param1
                process = subprocess.Popen(['python3', '/home/ubuntu/code/main.py', '--problem-id', problem.name, '--input', problem.inputfile, '--param1', param1])
                print('only one param')
            else:
                for param2 in comb_it2:
                    print(param2)
                    comb_it3 = comb_iterator(form.param3_start.data, form.param3_end.data, form.param3_step.data)
                    if comb_it3 is None:
                        # only start for param1 and param 2
                        process = subprocess.Popen(['python3', '/home/ubuntu/code/main.py', '--problem-id', problem.name, '--input', problem.inputfile, '--param1', param1, '--param2', param2])
                        print('two params')
                    else:
                        for param3 in comb_it3:
                            comb_it4 = comb_iterator(form.param4_start.data, form.param4_end.data,
                                                     form.param4_step.data)
                            if comb_it4 is None:
                                # only start for param1 and param 2
                                process = subprocess.Popen(
                                    ['python3', '/home/ubuntu/code/main.py', '--problem-id', problem.name, '--input', problem.inputfile, '--param1', param1, '--param2', param2, '--param3', param3])
                                print('three params')
                            else:
                                for param4 in comb_it4:
                                    comb_it5 = comb_iterator(form.param5_start.data, form.param5_end.data,
                                                             form.param5_step.data)
                                    if comb_it5 is None:
                                        # only start for param1 and param 2
                                        process = subprocess.Popen(
                                            ['python3', '/home/ubuntu/code/main.py', '--problem-id', problem.name, '--input', problem.inputfile, '--param1', param1, '--param2', param2,
                                             '--param3', param3, '--param4', param4])
                                    else:
                                        for param5 in comb_it5:
                                            process = subprocess.Popen(
                                                ['python3', '/home/ubuntu/code/main.py', '--problem-id', problem.name, '--input', problem.inputfile, '--param1', param1, '--param2', param2,
                                                 '--param3', param3, '--param4', param4, '--param5', param5])

        return redirect('/')
    return render_template('submit.html', form=form)


@app.route("/solution/<string:runid>")
def solutionReport(runid):
    result = Run.query.get(runid)
    return result.result


@app.route("/")
def hello():
    results = Run.query.order_by(Run.score.desc()).all()
    return render_template('home.html', results=results)

