from flask_restful import Resource, marshal, fields, reqparse
from flask import abort
from app import auth
from app.models import Meal, PatientMeal, MealRequirement
from sqlalchemy import func

meal_order_fields = {
    'id': fields.Integer,
    'label': fields.String,
    'total_orders': fields.Integer,
    'uri': fields.Url('meal'),
    'patients': fields.Url('patient_list_by_meal'),
    'requirements': fields.Url('requirement_list_by_meal')
}

meal_fields = {
    'id': fields.Integer,
    'label': fields.String,
    'total_quantity': fields.Integer,
    'current_quantity': fields.Integer,
    'uri': fields.Url('meal'),
    'patients': fields.Url('patient_list_by_meal'),
    'patient_meal': fields.Url('meal_list_by_patient'),
    'requirements': fields.Url('requirement_list_by_meal')
}


class MealResource(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        meal = Meal.query.get_or_404(id)
        return {'meal': marshal(meal, meal_fields)}


class MealListResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('feature', type=str, location=['json', 'args'])
        super(MealListResource, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()

        if args['feature'] == 'total_orders':
            meals = Meal.query(Meal.id, Meal.label, func.count(PatientMeal.id).label('total_orders')) \
                .join(PatientMeal) \
                .group_by(Meal.id, Meal.label) \
                .all()
            return {'meals': marshal([meal for meal in meals], meal_order_fields)}
        else:
            abort(400)
