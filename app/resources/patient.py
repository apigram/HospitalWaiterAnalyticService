from flask_restful import Resource, marshal, fields, reqparse
from flask import abort
from app import auth
from app.models import Patient

patient_fields = {
    'first_name': fields.String,
    'last_name': fields.String,
    'date_of_birth': fields.String,
    'uri': fields.Url('patient'),
}


class PatientResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, location='json')
        self.reqparse.add_argument('last_name', type=str, location='json')
        self.reqparse.add_argument('date_of_birth', type=str, location='json')
        super(PatientResource, self).__init__()

    def get(self, id):
        patient = Patient.query.get_or_404(id)
        return {'patient': marshal(patient, patient_fields)}


class PatientListResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, location='json')
        self.reqparse.add_argument('last_name', type=str, location='json')
        self.reqparse.add_argument('name', type=str, location='args')
        self.reqparse.add_argument('date_of_birth', type=str, location='json')
        self.reqparse.add_argument('email', type=str, location='json')
        super(PatientListResource, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        if args['feature'] is None:
            abort(404)

        patients = Patient.query.all()

        return {'patients': marshal([patient for patient in patients], patient_fields)}
