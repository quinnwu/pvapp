#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import random
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from settings import *

db = SQLAlchemy()

Judging = db.Table(
  'judging',
  db.Column('judge_id', db.Integer, db.ForeignKey('judge.id')),
  db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)

SecondRoundJudging = db.Table(
  'secondroundjudging',
  db.Column('judge_id', db.Integer, db.ForeignKey('judge.id')),
  db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)

Schools = db.Table(
  'schools',
  db.Column('member_id', db.Integer, db.ForeignKey('member.id')),
  db.Column('school_id', db.Integer, db.ForeignKey('school.id'))
)

class PastWinner(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  projectname = db.Column(db.String(100))
  info = db.Column(db.String(1000))
  photo = db.Column(db.String(50))
  year = db.Column(db.String(100))

class FrequentlyAsked(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  question = db.Column(db.String(1000))
  answer = db.Column(db.String(1000))

class Sponsors(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  prize = db.Column(db.String(200))
  photo = db.Column(db.String(50))

class MentorPhoto(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  position = db.Column(db.String(100))
  organization = db.Column(db.String(100))
  bio = db.Column(db.String(1000))
  photo = db.Column(db.String(50))
  
class SponsorPhoto(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(25))
  prize = db.Column(db.String(500))
  photo = db.Column(db.String(50))

class School(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(25))
  
  def __init__(self, name):
    self.name = name
  def __repr__(self):
    return '%s' % (self.name)

class Judge(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  cycle = db.Column(db.Integer) 
  name = db.Column(db.String(50))
  email = db.Column(db.String(120), unique=True)  
  pwdhash = db.Column(db.String(100))
  scores = db.relationship('Score', backref='judge', lazy='dynamic')
  semifinalistjudge = db.Column(db.Integer)
  secondroundscores = db.relationship('SecondRoundScore', backref='judge', lazy='dynamic')
  reviewing = db.relationship(
    'Project',
    secondary=Judging,
    backref=db.backref('judges', lazy='dynamic')
  )
  secondroundreviewing = db.relationship(
    'Project',
    secondary=SecondRoundJudging,
    backref=db.backref('secondroundjudges', lazy='dynamic')
  )
  def __repr__(self):
    return '%s' % (self.name)
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)
  def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.set_password(password)

  def first_round_subs_in_current_cycle(self):
    subs = []
    for project in reviewing:
      if(project.competitioncycle == COMPETITION_CYCLE):
        subs.append(project)
    return subs

  def second_round_subs_in_current_cycle(self):
    subs = []
    for project in secondroundreviewing:
      if(project.competitioncycle == COMPETITION_CYCLE):
        subs.append(project)
    return subs

  def setjudges(self):
    projects = Project.query.all()
    random.shuffle(projects)
    for each in projects:
      if (len(each.judges.all()) < 3) and (len(self.reviewing) < 3):
        self.reviewing.append(each)
      else:
        print "no new assignments, no no new"
  def setsecondjudges(self):
    projects = Project.query.filter_by(semifinalist = 2).all()
    random.shuffle(projects)
    for each in projects:
      if (len(each.secondroundjudges.all()) < 5) and (len(self.secondroundreviewing) < 5):
        self.secondroundreviewing.append(each)
        print "Success!"
      else:
        print "%s is reviewing %d submissions." % (self, len(self.secondroundreviewing))
        print "no new assignments, no no new"
  def __repr__(self):
    return '%s' % (self.name)

class Member(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  email = db.Column(db.String(120), unique=True)  
  phone = db.Column(db.String(20))
  pwdhash = db.Column(db.String(100))
  project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
  level = db.Column(db.String(20))
  year = db.Column(db.Integer)
  education = db.relationship(
    'School', 
    secondary=Schools, 
    backref=db.backref('students', lazy='dynamic')
  )
  
  def __init__(self, name, email, phone, password, education, level, year, project_id):
    self.name = name
    self.email = email
    self.year = year
    self.phone = phone
    self.project = Project.query.get(project_id)
    self.set_password(password)
    self.level = level
    for school in education:
      if School.query.filter(School.name == school).first():
        existingschool = School.query.filter(School.name == school).first()
        self.education.append(existingschool)
      else:
        newschool = School(school)
        self.education.append(newschool)

  def __repr__(self):
        return '%s' % (self.name)
 
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

class Score(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  judge_id = db.Column(db.Integer, db.ForeignKey('judge.id'))
  project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
  research = db.Column(db.Float) 
  innovation = db.Column(db.Float) 
  plan = db.Column(db.Float) 
  comment = db.Column(db.String(2000))
  weighted = db.Column(db.Float)
  def __init__(self, judgeid, projectid, researchscore, innovationscore, planscore, comment=""):
    self.judge_id = judgeid
    self.project_id = projectid
    self.research = researchscore
    self.innovation = innovationscore
    self.plan = planscore
    self.weighted = (researchscore + innovationscore + planscore)/3.0
    self.comment = comment
  def __repr__(self):
    return 'Score of %d for %s by %s' % (self.weighted, self.project, self.judge) 

class SecondRoundScore(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  judge_id = db.Column(db.Integer, db.ForeignKey('judge.id'))
  project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
  presentation = db.Column(db.Float) 
  innovation = db.Column(db.Float) 
  plan = db.Column(db.Float) 
  comment = db.Column(db.String(2000))
  weighted = db.Column(db.Float)
  def __init__(self, judgeid, projectid, presentationscore, innovationscore, planscore, comment=""):
    self.judge_id = judgeid
    self.project_id = projectid
    self.presentation = presentationscore 
    self.innovation = innovationscore
    self.plan = planscore
    self.weighted = (presentationscore + innovationscore + planscore)/3.0
    self.comment = comment
  def __repr__(self):
    return '2nd Round Score of %d for %s by %s' % (self.weighted, self.project, self.judge) 

class Project(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  submitted = db.Column(db.DateTime(timezone=True))
  competitioncycle = db.Column(db.Integer) # year of submission
  projectname = db.Column(db.String(50))
  description = db.Column(db.String(500))
  phaseone = db.Column(db.String(100))
  firstround = db.Column(db.Float())
  secondroundscore = db.Column(db.Float())
  semifinalist = db.Column(db.Integer) # 0 if not decided, 1 if not semifinalist, 2 if semifinalist, 3 if finalist 
  secondround = db.Column(db.String(200))
  members = db.relationship('Member', backref='project', lazy='dynamic') 
  scores = db.relationship('Score', backref='project', lazy='dynamic')
  secondroundscores = db.relationship('SecondRoundScore', backref='project', lazy='dynamic')
  finalpresentation = db.Column(db.String(100))
  def __init__(self, projectname, description):
    self.submitted = datetime.now()
    self.competitioncycle = self.submitted.year
    self.projectname = projectname
    self.description = description    
  
  def __repr__(self):
        return 'Project %s' % (self.projectname)

  def submitphaseone(self, phaseone):
    self.phaseone = phaseone
  def submitroundtwo(self, videolink):
    self.secondround = videolink 
  def submitfinalround(self, presentation):
    self.finalpresentation = presentation
  def updatesubmissiontime(self):
    self.submitted = datetime.now()
