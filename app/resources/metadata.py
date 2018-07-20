from flask_restful import Resource


class RequirementTypeList(Resource):
    def get(self):
        return {
            'requirement_types': [
                {'key': 'Allergen', 'value': 'ALLERGEN'},
                {'key': 'Positive', 'value': 'DIETARY_POSITIVE'},
                {'key': 'Negative', 'value': 'DIETARY_NEGATIVE'}
            ]
        }


class MealTimeList(Resource):
    def get(self):
        return {
            'meal_times': [
                {'key': 'Breakfast', 'value': 'BREAKFAST'},
                {'key': 'Lunch', 'value': 'LUNCH'},
                {'key': 'Dinner', 'value': 'DINNER'},
                {'key': 'Snack', 'value': 'SNACK'},
            ]
        }
