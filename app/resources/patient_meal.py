from flask_restful import Resource, marshal, fields, reqparse
from app import auth
from app.models import PatientMeal

# Viewed from patient details
meal_by_patient_fields = {
    'id': fields.Integer,
    'label': fields.String,
    'quantity': fields.Integer,
    'uri': fields.Url('meal_list_by_patient'),
    'meal': fields.Url('meal'),
    'requirements': fields.Url('requirement_list_by_patient'),
    'patient_meal': fields.Url('patient_meal')
}

# Viewed from meal details
patient_by_meal_fields = {
    'patient_name': fields.String,
    'quantity': fields.Integer,
    'uri': fields.Url('patient_list_by_meal'),
    'patient': fields.Url('patient'),
    'patient_meal': fields.Url('patient_meal')
}


class MealListByPatient(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('meal_id', type=int, required=True,
                                   help='No meal provided.', location='json')
        self.reqparse.add_argument('quantity', type=int, required=True,
                                   help='Quantity must be no lower than 1', location='json')
        super(MealListByPatient, self).__init__()

    def get(self, id):
        patient_meals = PatientMeal.query.filter_by(patient_id=id).all()
        meal_list = [{
            'id': patient_meal.id,
            'patient_id': patient_meal.patient_id,
            'meal_id': patient_meal.meal_id,
            'label': patient_meal.meal.label,
            'quantity': patient_meal.quantity
        } for patient_meal in patient_meals]

        return {'meals': marshal([meal for meal in meal_list], meal_by_patient_fields)}


class PatientListByMeal(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        patient_meals = PatientMeal.query.filter_by(meal_id=id).all()
        patient_list = [{
            'id': patient_meal.id,
            'patient_id': patient_meal.patient_id,
            'meal_id': patient_meal.meal_id,
            'patient_name': patient_meal.patient.first_name + ' ' + patient_meal.patient.last_name,
            'quantity': patient_meal.quantity
        } for patient_meal in patient_meals]

        return {'patients': marshal([meal for meal in patient_list], patient_by_meal_fields)}
