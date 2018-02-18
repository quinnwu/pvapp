#!/usr/bin/python
# -*- coding: utf-8 -*-
# from __future__ imports must be done at top
from __future__ import division
import os, sys
import binascii
import random
from settings import *
from pvapp import app
from flask import render_template, request, flash, session, url_for, redirect, send_from_directory
from forms import FinalRoundForm, ContactForm, SigninForm, CreateProjectForm, AddMemberForm, PhaseOneForm, AddJudgeForm, AddScoreForm, RoundTwoForm, AddSemifinalistScoreForm, AddMentorPhotoForm
from flask.ext.mail import Message, Mail
from models import db, Project, Member, Judge, MentorPhoto, PastWinner, FrequentlyAsked, Sponsors, Score, SecondRoundScore
from functools import wraps
from werkzeug import secure_filename
from datetime import datetime

mail = Mail()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not (('admin' in session) or ('project' in session) or ('judge' in session)):
            flash('Please first login.')
            return redirect(url_for('signin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def project_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'judge' in session:
          flash('That page is only for competitors. Sorry about that!')
          return redirect(url_for('profile'))
        if 'project' not in session:
            flash('Please first login.')
            return redirect(url_for('signin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def semifinalist_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'judge' in session:
          flash('That page is only for competitors. Sorry about that!')
          return redirect(url_for('profile'))
        if 'project' not in session:
            flash('Please first login.')
            return redirect(url_for('signin', next=request.url))
        else:
	    if not Project.query.get(session['project']).semifinalist == 2:
                flash('You are not a semifinalist. You may not submit a Round 2 Application!')
                return redirect(url_for('profile')) 
            return f(*args, **kwargs)
    return decorated_function

def finalist_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'judge' in session:
          flash('That page is only for competitors. Sorry about that!')
          return redirect(url_for('profile'))
        if 'project' not in session:
            flash('Please first login.')
            return redirect(url_for('signin', next=request.url))
        else:
	    if not Project.query.get(session['project']).semifinalist == 3:
                flash('You are not a finalist. Sorry!') 
                return redirect(url_for('profile')) 
            return f(*args, **kwargs)
    return decorated_function

def judge_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'judge' not in session:
            flash('You must be a judge to access this page.')
            return redirect(url_for('signin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            flash('You must be an admin to access this page.')
            return redirect(url_for('signin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
  static = app.config['UPLOAD_FOLDER']
  mentors = MentorPhoto.query.all()
  pastwinners = PastWinner.query.all()
  faqs = FrequentlyAsked.query.all()
  sponsors = Sponsors.query.all()
  return render_template('index.html', faqs=faqs, pastwinners=pastwinners, mentors=mentors, sponsors=sponsors, home="yes")

@app.route('/about')
def about():
  login = SigninForm() 
  return render_template('about.html', login=login)

@app.route('/news')
def news():
  return render_template('news.html')

@app.route('/addmentor', methods=['GET', 'POST'])
@admin_view
def addmentor():
  form = AddMentorPhotoForm()
  if form.validate_on_submit():
    filename = secure_filename(form.photo.data.filename)
    form.photo.data.save(os.path.join(app.config['STATIC_FOLDER'], filename))
    session['mentorphoto'] = form.getmentorphoto()
    db.session.commit()
    flash('You successfully added a mentor photo.')
    return redirect(url_for('mentors'))
  filename = None
  return render_template('addmentorphoto.html', form=form, filename=filename)

@app.route('/mentors', methods=['GET', 'POST'])
@admin_view
def mentors():
  mentors = MentorPhoto.query.all()
  return render_template('mentors.html', mentors=mentors)

@app.route('/5projects')
@admin_view
def fiveproj():
  projects = Project.query.filter(Project.submitted > ROUND_1_START_DATE, Project.submitted < ROUND_1_END_DATE)
  if projects.count() > 0:
    projects = projects.all()
    random.shuffle(projects)
    judges = Judge.query.all()
    for judge in judges:
      for each in projects:
        if (len(each.judges.all()) < 6) and (len(judge.reviewing) < 6):
          judge.reviewing.append(each)
          db.session.commit()
        else:
          print "no new assignments"
    return "Done!"
  else:
    return "No projects available."

@app.route('/secondroundjudges')
@admin_view
def secondroundjudges():
  judges = Judge.query.filter_by(semifinalistjudge = 1)
  for judge in judges:
    judge.setsecondjudges()
  db.session.commit()
  return "Done!"

@app.route('/semifinalistreminder')
@admin_view
def remindersemi():
  print "H"
  projects = Project.query.filter(Project.semifinalist == 2, Project.submitted > ROUND_1_START_DATE)
  print "THIS IS CHANGED"
  result = ""
  print "R"
  for each in projects:
    if not each.secondround:
      result += (each.projectname + "<BR />")
      for member in each.members:
        result += (member.email + "<BR />")
  return result 

@app.route('/semifinalistemails')
@admin_view
def emails():
  allproj = Project.query.order_by(Project.firstround.desc()).limit(70)
  for each in allproj:
    each.semifinalist = 1
    db.session.commit()
  projects = Project.query.order_by(Project.firstround.desc()).limit(21)
  result = ""
  for each in projects:
    result += ('<br /> <br />' + each.projectname + '<br />')
    each.semifinalist = 2
    db.session.commit()
    for member in each.members:
      result += (member.email + '<br />')
  return result

@app.route('/semifinalistpresentations')
@admin_view
def presentations():
  projects = Project.query.order_by(Project.firstround.desc()).limit(35)
  result = ""
  for each in projects:
    result += (each.projectname + ": http://pennvention.io/submission/" + each.phaseone + '<BR>')
  return result

@app.route('/firstroundscores')
@admin_view
def firstround():
  projects = Project.query.filter(Project.submitted > ROUND_1_START_DATE)
  result = ""
  for each in projects:
    scores = [s.weighted for s in each.scores.all()] 
    if len(scores):
      if len(scores) > 1:
        scores.remove(min(scores))
      if len(scores) > 1:
        scores.remove(min(scores))
      firstround = sum(scores)/len(scores)
      each.firstround = firstround
      db.session.commit()
      result += (each.projectname + " completed! %f \n" % (firstround)) 
  return result 

@app.route('/secondroundscores')
@admin_view
def secondroundscores():
  projects = Project.query.filter_by(semifinalist = 2)
  result = ""
  for each in projects:
    scores = [s.weighted for s in each.secondroundscores.all()] 
    if len(scores):
      secondround = sum(scores)/len(scores)
      each.secondroundscore = secondround 
      db.session.commit()
      result += (each.projectname + " completed! %f \n" % (secondround)) 
  return result 
@app.route('/login')
def login():
  loginform = SigninForm()
  return render_template('login.html', loginform=loginform)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  login = SigninForm() 
  form = ContactForm()
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form, login=login)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['nakavthekar@gmail.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template('contact.html', success=True, login=login)
  elif request.method == 'GET':
    return render_template('contact.html', form=form, login=login)

@app.route('/judgeregister', methods=['GET', 'POST'])
def judgeregister():
  login = SigninForm()
  form = AddJudgeForm()
  if form.validate_on_submit():
    session['judge'] = form.getjudge() 
    flash('You successfully registered as a Judge. Thanks for contributing to entrepreneurship at Penn!')
    return redirect(url_for('profile'))
  return render_template('registerjudge.html', form=form, login=login)

@app.route('/register', methods=['GET', 'POST'])
def register():
  if (('judge' in session) or ('admin' in session) or ('project' in session)):
    redirect(url_for('profile')) 
  login = SigninForm() 
  form = CreateProjectForm()
  if form.validate_on_submit():
    session['project'] = form.getproject() 
    flash('Congratulations! You successfully created your project. You can add the rest of your project members from "Actions" -> "Add Member".')
    return redirect(url_for('profile'))
  return render_template('register.html', form=form, login=login) 

@app.route('/judge/<int:project_id>', methods=['GET', 'POST'])
@judge_view
def judge_project(project_id):
  form = AddScoreForm()
  p = Project.query.get(project_id)
  if form.validate_on_submit():
    researchscore = form.newscore.data['researchscore']
    innovationscore = form.newscore.data['innovationscore']
    planscore = form.newscore.data['planscore']
    comment = form.newscore.data['comment']
    newscore = Score(session['judge'], project_id, researchscore, innovationscore, planscore, comment)
    db.session.add(newscore)
    db.session.commit()
    flash('You have successfully submitted a score!')
    return redirect(url_for('profile'))
  hasnotreviewed = 1
  for score in Score.query.filter_by(project_id = project_id).all():
    if (score.judge_id == session['judge']):
      hasnotreviewed = 0  
  if (Project.query.get(project_id) not in Judge.query.get(session['judge']).reviewing) and hasnotreviewed:
    j = Judge.query.get(session['judge'])
    flash('You did not have permission to view that project. Please select from the projects below that were assigned to you to judge.')
    return redirect(url_for('profile'))
  if not hasnotreviewed:
    flash('You have already reviewed this submission. If you believe this is in error, please email the judging coordinator at pennvention@gmail.com')
    return redirect(url_for('profile'))
  return render_template('judge.html', form=form, p=p, project_id=project_id)

@app.route('/2ndroundjudge/<int:project_id>', methods=['GET', 'POST'])
@judge_view
def judge2nd(project_id):
  form = AddSemifinalistScoreForm()
  p = Project.query.get(project_id)
  if form.validate_on_submit():
    presentationscore = form.newscore.data['presentationscore']
    innovationscore = form.newscore.data['innovationscore']
    planscore = form.newscore.data['planscore']
    comment = form.newscore.data['comment']
    newscore = SecondRoundScore(session['judge'], project_id, presentationscore, innovationscore, planscore, comment)
    db.session.add(newscore)
    db.session.commit()
    flash('You have successfully submitted a score!')
    return redirect(url_for('profile'))
  hasnotreviewed = 1
  for score in SecondRoundScore.query.filter_by(project_id = project_id).all():
    if (score.judge_id == session['judge']):
      hasnotreviewed = 0  
  if (Project.query.get(project_id) not in Judge.query.get(session['judge']).secondroundreviewing) and hasnotreviewed:
    j = Judge.query.get(session['judge'])
    flash('You did not have permission to view that project. Please select from the projects below that were assigned to you to judge.')
    return redirect(url_for('profile'))
  if not hasnotreviewed:
    flash('You have already reviewed this submission. If you believe this is in error, please email the judging coordinator at pennvention@gmail.com')
    return redirect(url_for('profile'))
  return render_template('2ndroundjudge.html', form=form, p=p, project_id=project_id)

@app.route('/addmember', methods=['GET', 'POST'])
@project_view
def addmember():
  form = AddMemberForm()
  if form.validate_on_submit():
    flash('You have successfully added a member!')
    return redirect(url_for('profile'))
  return render_template('addmember.html', form=form)  

@app.route('/signin', methods=['POST'])
def signin():
  login = SigninForm() 
  if ('project' in session) or ('judge' in session):
    return redirect(url_for('profile')) 
  if login.validate_on_submit(): # means that user is either judge or project member 
    if login.findmember():
      session['project'] = login.getproject() # sets to id of project 
      if Project.query.get(session['project']).semifinalist >= 2:
        session['semifinalist'] = True
    elif login.findjudge():
      session['judge'] = login.findjudge() # sets to id of judge
    elif login.findadmin():
      session['admin'] = login.findadmin()
    return redirect(url_for('profile'))
  flash('Incorrect login details. Please try again or register for a new account.')
  return redirect(url_for('login')) 

@app.route('/profile')
@login_required
def profile():
  if 'project' in session:
    p = Project.query.get(session['project'])
    members = p.members.all()
    scores = [s.weighted for s in p.scores.all()] 
    comments = [s.comment for s in p.scores.all()]
    secondroundcomments = [s.comment for s in p.secondroundscores.all()]
    return render_template('profile.html', p = p, comments = comments, secondroundcomments = secondroundcomments, members=members)
  elif 'judge' in session:
    j = Judge.query.get(session['judge'])
    return render_template('judgeprofile.html', j=j, COMPETITION_CYCLE=COMPETITION_CYCLE)
  elif 'admin' in session:
    projects = Project.query.all()
    projects_t = Project.query.filter(Project.submitted > ROUND_1_START_DATE)
    return render_template('adminprofile.html', projects=projects_t)

@app.route('/phaseone/', methods=('GET', 'POST'))
@project_view
def phaseone():
  if datetime.now() > ROUND_1_START_DATE and datetime.now() < ROUND_1_END_DATE:
    form = PhaseOneForm()
    print "here1"
    if form.validate_on_submit():
        print "here2"
        filename = secure_filename(form.presentation.data.filename)
        print filename
        form.presentation.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print "here3"
        p = Project.query.get(session['project'])
        print p
        p.submitphaseone(filename) 
        p.updatesubmissiontime()
        db.session.commit()
        flash("You have successfully submitted your Round 1 Presentation! Stay tuned for judging results, which should arrive in approximately 2 weeks.")
        return redirect(url_for('profile'))
    filename = None
    return render_template('phaseone.html', form=form, filename=filename, open=True) 
  else:
    form = PhaseOneForm()
    filename = None
    return render_template('phaseone.html', form=form, filename=filename, open=False)
  
@app.route('/roundtwo/', methods=('GET', 'POST'))
@semifinalist_view
def roundtwo():
  form = RoundTwoForm()
  if form.validate_on_submit():
    videolink = form.videolink.data 
    p = Project.query.get(session['project'])
    p.submitroundtwo(videolink) 
    p.updatesubmissiontime()
    db.session.commit()
    flash("You have successfully submitted your Round Two Video Pitch! Stay tuned for Finalist results, which should be in within the week!")
    return redirect(url_for('profile'))
  return render_template('roundtwo.html', form=form) 

@app.route('/finalround', methods=('GET', 'POST'))
@finalist_view
def finalround():
  form = FinalRoundForm()
  if form.validate_on_submit():
    filename = secure_filename(form.presentation.data.filename)
    form.presentation.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    p = Project.query.get(session['project'])
    p.submitfinalround(filename) 
    p.updatesubmissiontime()
    db.session.commit()
    flash("You have successfully submitted your Final Round Video Pitch! See you on Monday!")
    return redirect(url_for('profile'))
  filename = None
  return render_template('finalround.html', form=form, filename=filename)


@app.route('/submission/<filename>') 
def submission(filename): 
  return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename)

@app.route('/signout')
@login_required
def signout():
  session.pop('project', None)
  session.pop('judge', None)
  session.pop('admin', None)
  return redirect(url_for('home'))

if __name__ == '__main__':
  	app.run(host='0.0.0.0')
