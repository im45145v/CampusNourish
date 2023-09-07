from pymongo import MongoClient

mongostr = ""
client = MongoClient(mongostr, serverSelectionTimeoutMS=60000)
db = client['HacksForU']

def show_roadmaps():
    Roadmaps = db["Roadmaps"]
    roadmaps = iter(Roadmaps.find())
    return roadmaps

def show_courses():
    Courses = db["Courses"]
    courses = iter(Courses.find())
    return courses

def show_FreeStuff():
    FreeStuff = db["FreeStuff"]
    items = iter(FreeStuff.find())
    return items

def create_roadmap(Title,Description,Image,Link):
    Roadmaps = DB["Roadmaps"]
    new_roadmap = {
        "Title": Title,
        "Description": Description,
        "Image" : Image,
        "Link": Link        
        }
    Roadmaps.insert_one(new_roadmap)

def create_FreeStuff(Title,Description,Image,Link):
    FreeStuff = DB["FreeStuff"]
    new_stuff = {
        "Title": Title,
        "Description": Description,
        "image" : Image,
        "Link": Link        
    }
    FreeStuff.insert_one(new_stuff)

def create_courses(Title,Description,Image,Link):
    Courses = DB["Courses"]
    new_course = {
        "Title": Title,
        "Description": Description,
        "image" : Image,
        "Link": Link        
    }
    Courses.insert_one(new_course)
