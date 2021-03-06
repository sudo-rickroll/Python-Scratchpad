import numpy as np
from collections import namedtuple
import datetime, decimal
from faker import Faker
from time import perf_counter

def fake_profiles(profiles, mode):
  """
  Decorator Factory
  Args:
      profiles: Number of profiles to fetch from faker
      mode : 'dict' for adding the required parameters from the faker profile to a dict, 'namedtuple' to add them to a namedtuple

  Returns:
      Decorator that decorates the function and provides it with an array containing the details to be included from the fake profile   
  """

  from functools import wraps
  fake = Faker()
  fake_array = []
  def decorator(fn):  
    if mode == 'namedtuple':
      Fake = namedtuple('Fake', 'Name Blood_Group Location Age')
      for i in range(profiles):
        profile = fake.profile()
        fake_array.append(Fake(profile['name'], profile['blood_group'], profile['current_location'], (datetime.date.today() - profile['birthdate']).days / 365))
    elif mode == 'dict':
      for i in range(profiles):
        profile = fake.profile()
        fake_array.append({"Name" : profile['name'], "Blood_Group" : profile['blood_group'], "Location" : profile['current_location'], "Age" : (datetime.date.today() - profile['birthdate']).days / 365})
    else:
      raise ValueError("Mode only takes 'dict' or 'namedtuple' values ")
    @wraps(fn)
    def inner(fake_array = fake_array):
      start = perf_counter()
      result = fn(fake_array)
      end = perf_counter()
      print(f"\n\033[3mFunction '{fn.__name__}' took {end - start} seconds to complete\033[0m\n")
      return result
    return inner
  return decorator

@fake_profiles(10000,'namedtuple')
def calculate_stats_namedtuple(arr):
  
  age_array = [i.Age for i in arr]
  average_location = (np.mean(np.array([i.Location[0] for i in arr])), np.mean(np.array([i.Location[1] for i in arr])))    
  if len(np.where(np.array(age_array) == sorted(age_array)[0])[0]) == 1:
    oldest_person_profile = arr[np.where(np.array(age_array) == sorted(age_array, reverse=True)[0])[0][0]]
  elif len(np.where(np.array(age_array) == sorted(age_array)[0])[0]) > 1:
    oldest_person_profile = []
    oldest_person_profile.extend([arr[i] for i in np.where(np.array(age_array) == sorted(age_array, reverse=True)[0])[0]])
  average_age = np.mean(np.array(age_array))
  oldest_age = [profile.Age for profile in oldest_person_profile] if isinstance(oldest_person_profile, list) else oldest_person_profile.Age
  most_common_bloodgroup = arr[np.argmax(np.unique(np.array([i.Blood_Group for i in arr]), return_counts=True)[1])].Blood_Group
  if isinstance(oldest_person_profile, list):
    for profile in oldest_person_profile:
        print(f"Oldest person {profile.Name}'s age is {int(profile.Age)} Years,{(profile.Age - int(profile.Age)) * 12 : .1f} Months")
  else:
    print(f"Oldest person {oldest_person_profile.Name}'s age is {int(oldest_age)} Years,{(oldest_age - int(oldest_age)) * 12 : .1f} Months")
  print(f"Average age is {int(average_age)} Years,{(average_age - int(average_age)) * 12 : .1f} Months")
  print(f"Average Location coordinates is at {average_location[0]}, {average_location[1]}")
  print(f"Most common blood group among the profiles is {most_common_bloodgroup}")
  return most_common_bloodgroup, average_location, oldest_age, average_age

@fake_profiles(10000,'dict')
def calculate_stats_dict(arr):

  age_array = [i['Age'] for i in arr]
  average_location = (np.mean(np.array([i['Location'][0] for i in arr])), np.mean(np.array([i['Location'][1] for i in arr])))       
  if len(np.where(np.array(age_array) == sorted(age_array)[0])[0]) == 1:
    oldest_person_profile = arr[np.where(np.array(age_array) == sorted(age_array, reverse=True)[0])[0][0]]
  elif len(np.where(np.array(age_array) == sorted(age_array)[0])[0]) > 1:
    oldest_person_profile = []
    oldest_person_profile.extend([arr[i] for i in np.where(np.array(age_array) == sorted(age_array, reverse=True)[0])[0]])
  average_age = np.mean(np.array(age_array))
  oldest_age = [profile['Age'] for profile in oldest_person_profile] if isinstance(oldest_person_profile, list) else oldest_person_profile['Age']
  most_common_bloodgroup = arr[np.argmax(np.unique(np.array([i['Blood_Group'] for i in arr]), return_counts=True)[1])]['Blood_Group']   
  if isinstance(oldest_person_profile, list):
    for profile in oldest_person_profile:
        print(f"Oldest person {profile['Name']}'s age is {int(profile['Age'])} Years,{(profile['Age'] - int(profile['Age'])) * 12 : .1f} Months")
  else:
    print(f"Oldest person {oldest_person_profile['Name']}'s age is {int(oldest_age)} Years,{(oldest_age - int(oldest_age)) * 12 : .1f} Months")
  print(f"Average age is {int(average_age)} Years,{(average_age - int(average_age)) * 12 : .1f} Months")
  print(f"Average Location coordinates is at {average_location[0]}, {average_location[1]}")
  print(f"Most common blood group among the profiles is {most_common_bloodgroup}")
  return most_common_bloodgroup, average_location, oldest_age, average_age
