
from mongoengine import connect, get_db
connect(
    host='mongodb+srv://root:12345@cluster0.kv3gwol.mongodb.net/school'
)
db= get_db()
def exist(grade):
    query=db.grade.find({'grade':grade}).limit(1).size()
    return query
