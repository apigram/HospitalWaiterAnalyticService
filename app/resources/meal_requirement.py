from flask_restful import Resource, marshal, fields, reqparse
from app import db, auth
from app.models import MealRequirement

# Viewed from requirement details
meal_by_requirement_fields = {
    'id': fields.Integer,
    'label': fields.String,
    'scale': fields.String,
    'uri': fields.Url('meal_list_by_requirement'),
    'meal': fields.Url('meal'),
}

# Viewed from meal details
requirement_by_meal_fields = {
    'id': fields.Integer,
    'label': fields.String,
    'scale': fields.String,
    'type': fields.String,
    'uri': fields.Url('requirement_list_by_meal'),
    'requirement': fields.Url('requirement'),
    'requirement_meal': fields.Url('meal_requirement')
}


class MealListByRequirement(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        requirement_meals = MealRequirement.query.filter_by(requirement_id=id).all()
        meal_list = [{
            'id': requirement_meal.id,
            'requirement_id': requirement_meal.requirement_id,
            'meal_id': requirement_meal.meal_id,
            'label': requirement_meal.meal.label,
            'scale': requirement_meal.scale
        } for requirement_meal in requirement_meals]

        return {'meals': marshal([meal for meal in meal_list], meal_by_requirement_fields)}


class RequirementListByMeal(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('requirement_id', type=int, required=True,
                                   help='No requirement specified.', location='json')
        self.reqparse.add_argument('scale', type=str, location='json')
        super(RequirementListByMeal, self).__init__()

    def get(self, id):
        requirement_meals = MealRequirement.query.filter_by(meal_id=id).all()
        requirement_list = [{
            'id': requirement_meal.id,
            'requirement_id': requirement_meal.requirement_id,
            'meal_id': requirement_meal.meal_id,
            'label': requirement_meal.requirement.label,
            'scale': requirement_meal.scale,
            'type': requirement_meal.requirement.type
        } for requirement_meal in requirement_meals]

        return {'requirements': marshal([meal for meal in requirement_list], requirement_by_meal_fields)}

    def post(self, id):
        args = self.reqparse.parse_args()
        meal = MealRequirement()
        meal.meal_id = id
        meal.requirement_id = args['requirement_id']
        if 'scale' in args:
            meal.scale = args['scale']
        db.session.add(meal)
        db.session.commit()
        meal_req = {
            'id': meal.id,
            'meal_id': meal.meal_id,
            'requirement_id': meal.requirement_id,
            'label': meal.requirement.label,
            'scale': meal.scale,
            'type': meal.requirement.type
        }
        return {'requirement': marshal(meal_req, requirement_by_meal_fields)}, 201
