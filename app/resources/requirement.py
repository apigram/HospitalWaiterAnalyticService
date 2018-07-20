from flask_restful import Resource, marshal, fields, reqparse
from flask import abort
from app import auth
from sqlalchemy import func
from app.models import Requirement, MealRequirement, Meal, PatientMeal, PatientRequirement

requirement_meal_order_fields = {
    'id': fields.Integer,
    'label': fields.String,
    'total_meals_ordered': fields.Integer,
    'uri': fields.Url('meal'),
}

patient_requirement_fields = {
    'id': fields.Integer,
    'label': fields.String,
    'total_patients': fields.Integer,
    'uri': fields.Url('meal'),
}

requirement_fields = {
    'id': fields.Integer,
    'label': fields.String,
    'type': fields.String,
    'uri': fields.Url('requirement'),
    'patients': fields.Url('patient_list_by_requirement'),
    'meals': fields.Url('meal_list_by_requirement')
}


class RequirementResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('label', type=str, location='json')
        self.reqparse.add_argument('type', type=str, location='json')
        super(RequirementResource, self).__init__()

    def get(self, id):
        requirement = Requirement.query.get_or_404(id)
        return {'requirement': marshal(requirement, requirement_fields)}


class RequirementListResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('feature', type=str, location=['json', 'args'])
        super(RequirementListResource, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()

        if args['feature'] == 'total_meals_ordered':
            meals = Requirement.query(Requirement.id,
                                      Requirement.label,
                                      func.count(PatientMeal.id).label('total_meals_ordered')) \
                .join(MealRequirement) \
                .join(Meal) \
                .join(PatientMeal) \
                .group_by(Requirement.id, Requirement.label) \
                .all()
            return {'meals': marshal([meal for meal in meals], requirement_meal_order_fields)}
        elif args['feature'] == 'total_patients':
            meals = Requirement.query(Requirement.id,
                                      Requirement.label,
                                      func.count(PatientRequirement.id).label('total_patients')) \
                .join(PatientRequirement) \
                .group_by(Requirement.id, Requirement.label) \
                .all()
            return {'meals': marshal([meal for meal in meals], patient_requirement_fields)}
        else:
            abort(400)
