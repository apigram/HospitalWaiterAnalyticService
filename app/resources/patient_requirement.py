from flask_restful import Resource, marshal, fields, reqparse
from app import auth
from app.models import PatientRequirement

# Viewed from patient details
requirement_by_patient_fields = {
    'id': fields.Integer,
    'label': fields.String,
    'type': fields.String,
    'scale': fields.String,
    'uri': fields.Url('requirement_list_by_patient'),
    'requirement': fields.Url('requirement'),
    'patient_requirement': fields.Url('patient_requirement')
}

# Viewed from requirement details
patient_by_requirement_fields = {
    'id': fields.Integer,
    'patient_name': fields.String,
    'scale': fields.String,
    'uri': fields.Url('patient_list_by_requirement'),
    'patient': fields.Url('patient'),
    'patient_requirement': fields.Url('patient_requirement')
}


class RequirementListByPatient(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('requirement_id', type=int, required=True,
                                   help='No requirement provided.', location='json')
        self.reqparse.add_argument('scale', type=str, location='json')
        super(RequirementListByPatient, self).__init__()

    def get(self, id):
        patient_requirements = PatientRequirement.query.filter_by(patient_id=id).all()
        requirement_list = [{
            'id': patient_requirement.id,
            'patient_id': patient_requirement.patient_id,
            'requirement_id': patient_requirement.requirement_id,
            'label': patient_requirement.requirement.label,
            'type': patient_requirement.requirement.type,
            'scale': patient_requirement.scale
        } for patient_requirement in patient_requirements]

        return {'requirements': marshal([requirement for requirement in requirement_list], requirement_by_patient_fields)}


class PatientListByRequirement(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        patient_requirements = PatientRequirement.query.filter_by(requirement_id=id).all()
        patient_list = [{
            'id': patient_requirement.id,
            'patient_id': patient_requirement.patient_id,
            'requirement_id': patient_requirement.requirement_id,
            'patient_name': patient_requirement.patient.first_name + ' ' + patient_requirement.patient.last_name,
            'scale': patient_requirement.scale
        } for patient_requirement in patient_requirements]

        return {'patients': marshal([requirement for requirement in patient_list], patient_by_requirement_fields)}
