from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import bcrypt
import re
name_regex = re.compile(r'^[A-Za-z]{3}')
password_regex = re.compile(r'^.{8}')
# Create your models here.
class LoginManager(models.Manager):
	def register(self, name, username, passw, confirm):
		errors = []
		if not name_regex.match(name):
			errors.append('Name must be no fewer than 3 characters and letters only')
		if not name_regex.match(username):
			errors.append('Username must be no fewer than 3 characters and letters only')
		if not password_regex.match(passw):
			errors.append('password must be no fewer than 8 characters')
		if passw != confirm:
			errors.append('passwords must match')
		if len(errors) != 0:
			return (False, errors)
		else:
			passw = passw.encode()
			hashed = bcrypt.hashpw(passw, bcrypt.gensalt())
			e = Users.loginmgr.create(name = name, username = username, password = hashed)
			e.save()
			return (True, e)
	def login(self, username, password):
		errors = []
		try:
			result = Users.loginmgr.get(username = username)
		except:
			errors.append('please enter a valid username')
			return (False, errors)
		if not bcrypt.hashpw(password.encode(), result.password.encode()) == result.password.encode():
			errors.append('password is incorrect')
			return (False, errors)
		return (True, result)

class Users(models.Model):
	name = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	loginmgr = LoginManager()

class Wishes(models.Model):
	user_id = models.ManyToManyField(Users, related_name = 'wishuserid')
	item = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
