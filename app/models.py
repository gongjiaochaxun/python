from gongjiao.settings import MONGODB_INFO
from mongoengine import connect, fields, Document


connect(MONGODB_INFO['DATABASE'],
        username=MONGODB_INFO['USERNAME'],
        password=MONGODB_INFO['PASSWORD'],
        host=MONGODB_INFO['URI'],
        connect=False)

class User(Document):
    meta = {
        'index_background': True,
        'auto_create_index': True,
        'collection': 'users'
    }
    username = fields.StringField(required=True)
    password = fields.StringField(required=True)
    email = fields.StringField(required=True)
    sex = fields.StringField(required=True)
    role = fields.StringField(required=True)


class Place(Document):
    meta = {
        'index_background': True,
        'auto_create_index': True,
        'collection': 'places'
    }
    placename = fields.StringField(required=True)
    routes = fields.ListField(fields.ReferenceField('Route'),default=[])

    def add_route(self, route: 'Route') -> 'Place':
        if route not in self.routes:
            self.routes.append(route)
            self.save()
        return self

    def del_route(self, route: 'Route') -> 'Place':
        if route in self.routes:
            self.routes.remove(route)
            self.save()
        if self in route.places:
            route.del_place(self)
            route.save()
        return self

class Route(Document):
    meta = {
        'index_background': True,
        'auto_create_index': True,
        'collection': 'routes'
    }
    routename = fields.StringField(required=True)
    places = fields.ListField(fields.ReferenceField('Place'),default=[])
    money = fields.StringField(required=True)
    start_time = fields.StringField(requires=True)
    stop_time = fields.StringField(required=True)

    def add_place(self, place: 'Place', pos: 'int') -> 'Route':
        if place not in self.places:
            self.places.insert(pos, place)
            self.save()
            place.add_route(self, pos)
            place.save()
        return self

    def del_place(self, place: 'Place') -> 'Route':
        if place in self.places:
            self.places.remove(place)
            self.save()
        if self in place.routes:
            place.del_route(self)
            place.save()
        return self


