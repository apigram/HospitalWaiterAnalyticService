from app import app
from flask_restful import Api
from app.resources.meal import MealResource, MealListResource
from app.resources.patient import PatientResource, PatientListResource
from app.resources.requirement import RequirementResource, RequirementListResource
from app.resources.patient_meal import MealListByPatient, PatientListByMeal
from app.resources.patient_requirement import PatientListByRequirement, RequirementListByPatient
from app.resources.meal_requirement import MealListByRequirement, RequirementListByMeal
from app.resources.auth import TokenResource

api = Api(app)

# Simple list/base resources
api.add_resource(MealListResource, '/biservice/meal',
                 endpoint='meals')
api.add_resource(MealResource, '/biservice/meal/<int:id>',
                 endpoint='meal')

api.add_resource(PatientListResource, '/biservice/patient',
                 endpoint='patients')
api.add_resource(PatientResource, '/biservice/patient/<int:id>',
                 endpoint='patient')

api.add_resource(RequirementListResource, '/biservice/requirement',
                 endpoint='requirements')
api.add_resource(RequirementResource, '/biservice/requirement/<int:id>',
                 endpoint='requirement')

# Composite resources
api.add_resource(MealListByPatient, '/mealservice/patient/<int:id>/meal',
                 endpoint='meal_list_by_patient')
api.add_resource(PatientListByMeal, '/mealservice/meal/<int:id>/patient',
                 endpoint='patient_list_by_meal')

api.add_resource(RequirementListByPatient, '/mealservice/patient/<int:id>/requirement',
                 endpoint='requirement_list_by_patient')
api.add_resource(PatientListByRequirement, '/mealservice/requirement/<int:id>/patient',
                 endpoint='patient_list_by_requirement')

api.add_resource(MealListByRequirement, '/mealservice/requirement/<int:id>/meal',
                 endpoint='meal_list_by_requirement')
api.add_resource(RequirementListByMeal, '/mealservice/meal/<int:id>/requirement',
                 endpoint='requirement_list_by_meal')

# Token resource
api.add_resource(TokenResource, '/biservice/auth/token', endpoint='auth_token')
