from enum import Enum
from datetime import datetime, timedelta
from django.db import models

# Create your models here.

# class PetType(Enum):
#     DOG = 'dog'
#     CAT = 'cat'
#     FISH = 'fish'
#     SMALL = 'small'
#     BIRD = 'bird'
#     REPTILE = 'reptile'

class PersonRole(Enum):
    VET = "vet"
    OWNER = "owner"
    SITTER = "sitter"

class Pet:
    def __init__(self, id, name, type, breed, sex, dob, weight, spayed, vet, owner, conditions, vaccines, lastUpdated, relation):
        self.id = id
        self.name = name
        self.type = type
        self.breed = breed
        self.sex = sex
        self.dob = dob
        self.weight = weight
        self.spayed = spayed
        self.vet = vet
        self.owner = owner
        self.conditions = conditions
        self.vaccines = vaccines
        self.lastUpdated = lastUpdated
        self.relation = relation

class Person:
    def __init__(self, id, role, firstName, lastName, phone, email, address, city, state, zip_code=""):
        self.id = id
        self.role = role
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zip_code

class Condition:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

class Vaccine:
    def __init__(self, id, name, last_done, next_due):
        self.id = id
        self.name = name
        self.lastDone = last_done
        self.nextDue = next_due

class FeedItem:
    def __init__(self, id, title, description, pet, comments, date_created=datetime.today(), is_solved=False):
        self.id = id
        self.title = title
        self.description = description
        self.pet = pet
        self.comments = comments
        self.dateCreated = date_created
        self.isSolved = is_solved

vet = Person(
    1,
    PersonRole.VET,
    "Jane",
    "Doe",
    "123-456-7890",
    "janedoe@vet.com",
    "123 Wallaby Way",
    "Anywhere",
    "VA",
    "12345"
)

owner01 = Person(
    2,
    PersonRole.OWNER,
    "John",
    "Smith",
    "555-555-5555",
    "johnsmith@owner.com",
    "101 Evergreen Dr",
    "Anywhere",
    "VA",
    "12345"
)

owner02 = Person(
    3,
    PersonRole.OWNER,
    "George",
    "Washington",
    "987-654-3210",
    "gwash@owner.com",
    "102 Evergreen Dr",
    "Anywhere",
    "VA",
    "12345"
)

owner03 = Person(
    4,
    PersonRole.OWNER,
    "Dove",
    "Perry",
    "333-333-3333",
    "doveperry@owner.com",
    "103 Evergreen Dr",
    "Anywhere",
    "VA",
    "12345"
)

diet01 = Condition(
    1,
    "Diet",
    "Willow is currently being fed 1 cup of Black Gold Puppy Food twice a day."
)

allergies01 = Condition(
    2,
    "Allergies",
    "Willow suffers from season allergies in the Spring and Fall. Her allergies cause her to be itchy and to have yeast infections in her ears. If this happens, wash her ears out with ear wash and give her 10 mg of Zyrtec once daily until symptoms subside."
)

conditions01 = [diet01, allergies01]

vac1 = Vaccine(
    1,
    "Bordetella Vaccine",
    datetime(year=2024, month=7, day=22),
    datetime(year=2025, month=7, day=22)
)

vac2 = Vaccine(
    2,
    "Lyme Disease",
    datetime(year=2024, month=8, day=16),
    datetime(year=2025, month=8, day=16)
)

vac3 = Vaccine(
    3,
    "Rabies Vaccine",
    datetime(year=2024, month=8, day=16),
    datetime(year=2025, month=8, day=16)
)

vaccines = [vac1, vac2, vac3]

pet01 = Pet(
    1,
    "Willow",
    "dog",
    "Golden Retriever",
    "Female",
    datetime(year=2024, month=4, day=28),
    54.0,
    True,
    vet,
    owner01,
    conditions01,
    vaccines,
    datetime(year=2025, month=2, day=20),
    "owner"
)

pet02 = Pet(
    2,
    "Garfield",
    "cat",
    "Orange Tabby",
    "Male",
    datetime(year=2018, month=12, day=26),
    12.4,
    True,
    vet,
    owner01,
    conditions01,
    vaccines,
    datetime(year=2025, month=1, day=12),
    "owner"
)

pet03 = Pet(
    3,
    "Maggie",
    "dog",
    "Labrador Retriever",
    "Female",
    datetime(year=2019, month=5, day=8),
    55.6,
    True,
    vet,
    owner02,
    conditions01,
    vaccines,
    datetime(year=2025, month=2, day=17),
    "client"
)

pet04 = Pet(
    4,
    "Farfetch'd",
    "bird",
    "Conure",
    "Male",
    datetime(year=2023, month=2, day=26),
    0.28,
    False,
    vet,
    owner03,
    conditions01,
    vaccines,
    datetime(year=2024, month=11, day=22),
    "client"
)

pet05 = Pet(
    5,
    "Snoopy",
    "dog",
    "Beagle",
    "Male",
    datetime(year=2021, month=10, day=26),
    27.1,
    True,
    vet,
    owner02,
    conditions01,
    vaccines,
    datetime(year=2024, month=12, day=2),
    "client"
)

pets = [pet01, pet02, pet03, pet04, pet05]

vetFeedItem01 = FeedItem(
    1,
    "My puppy won't stop nipping and biting",
    "My puppy constantly nips at me and guests. I don't want it to escalate to breaking skin. What should I do?",
    pet01,
["comment 1", "comment 2"],
    datetime.now()
)

vetFeedItem02 = FeedItem(
    2,
    "My cat has a runny nose",
    "My indoor cat has had a runny nose for the pasty 2 days. Should I be concerned?",
    pet02,
    ["comment 1", "comment 2"],
    datetime.now() - timedelta(minutes=15)
)

vetFeedItem03 = FeedItem(
    3,
    "My bird chipped his beak",
    "I know birds can chip their beaks naturally, but I want to make sure my bird is okay. Is there anything I should do to help him?",
    pet04,
    ["comment 1", "comment 2"],
    datetime.now() - timedelta(hours=1, minutes=20)
)

vetFeed = [vetFeedItem01, vetFeedItem02, vetFeedItem03]

feedItem01 = FeedItem(
    4,
    "Willow's weight has changed",
    "Willow's weight has increased from 41.1 lbs to 54 lbs",
    pet01,
    ["comment 1", "comment 2"],
    datetime.today()
)

feedItem02 = FeedItem(
    5,
    "Maggie's food has changed",
    "Maggie's food has changed from Purina Pro Plan to Royal Canine. She should be feed 2 1/2 cups per day.",
    pet03,
    ["comment 1", "comment 2", "comment 3", "comment 4", "comment 5"],
    datetime.today() + timedelta(days=1, hours=3, minutes=5)
)

feedItem03 = FeedItem(
    6,
    "Maggie had a vet appointment",
    "See Maggie's pet profile for note from vet.",
    pet03,
    [],
    datetime.today() + timedelta(days=1, hours=3, minutes=20)
)

ownerFeed = [feedItem01, feedItem02, feedItem03]

owner_user = {"username": "john", "password": "owner"}
vet_user = {"username": "jane", "password": "vet"}