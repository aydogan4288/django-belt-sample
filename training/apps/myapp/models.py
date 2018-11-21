from django.db import models
import re
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        if len(postData['name']) < 3:
            errors['name'] = 'Name must contain at least 2 characters!'
        # elif not NAME_REGEX.match(postData['name']):
        #     errors['name'] = 'Name must contain only letters!'

        if len(postData['username']) < 3:
            errors['username'] = 'Username must contain at least 3 characters!'

        if len(postData['username']) < 1:
            errors['username'] = 'You muts provide an username!'
        elif User.objects.filter(username=postData['username']):
            errors['username'] = "username is already taken."

        if len(postData['password']) <2 :
            errors['password'] = 'Password must contain at least 8 characters'
        if postData['confirm'] != postData['password']:
            errors['confirm'] = 'Password confirmation doesn not match the Password!'

        return errors

    def login_validator(self, postData):
        errors = {}

        if len(postData['passwordlogin']) < 1:
            errors['passwordlogin'] = "Password cannot be blank."

        if len(postData['usernamelogin']) < 1:
            errors['usernamelogin'] = "Username cannot be blank."
        elif not User.objects.filter(username=postData['usernamelogin']):
            errors['usernamelogin'] = "Username is not in database."

        else:
            user = User.objects.filter(username=postData['usernamelogin'])
            print(user)
            if not bcrypt.checkpw(postData['passwordlogin'].encode(), user[0].password.encode()):
                errors['passwordlogin'] = "Passwords don't match"
        return errors
#
class TripManager(models.Manager):
	def trip_validator(self, postData):
		errors = {}

		if len(postData['destination']) < 2:
			errors['destination'] = "Destination must contain more than two characters"

		if not postData['travel_start_date']:
			errors['travel_start_date'] = "Travel Start Date cannot be blank"
		elif postData['travel_start_date'] < str(datetime.now()):
			errors['travel_start_date'] = "Start date must be a future date!"

		if not postData['travel_end_date']:
			errors['travel_end_date'] = "Travel Start Date cannot be blank"
		elif postData['travel_end_date'] < postData['travel_start_date']:
			errors['travel_end_date'] = "End date must be later than Start Date!"
		return errors


# class TripManager(models.Manager):
#     def trip_validator(self, postData):
#
#         if len(postData['destination']) < 1:
#             errors['destination'] = 'You must provide a Destination!'
#         if len(postData['plan']) < 5:
#             errors['plan'] = 'Descrtiption must contain at least 5 characters!'
#         if postData['travel_start_date'] < str(datetime.now()):
#             errors['travel_start_date'] = 'Travel Start Date must be a future date!'
#         if postData['travel_end_date'] < postData['travel_end_date']:
#             errors['travel_end_date'] = 'Travel End Date must be later than Travel Start Date!'
#
#         return errors


class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # Created Trips ---> One To Many
    # Joined Travels ---> Many To Many
    objects = UserManager()
    def __str__(self):
        return self.username

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    plan = models.TextField()
    travel_start_date = models.DateTimeField()
    travel_end_date = models.DateTimeField()
    joined_users = models.ManyToManyField(User, related_name="joined_travels")
    creater = models.ForeignKey(User, related_name="created_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = TripManager()
    def __str__(self):
        return self.destination
