from flask_restful import Resource, marshal, fields, reqparse
from flask import abort
from app import auth
from app.models import Dataset, Datapoint

dataset_fields = {
    'name': fields.String,
    'uri': fields.Url('dataset'),
    'datapoints': fields.Url('datapoints')
}

datapoint_fields = {
    'name': fields.String,
    'uri': fields.Url('datapoint')
}


class DatasetResource(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        dataset = Dataset.query.get_or_404(id)
        return {'dataset': marshal(dataset, dataset_fields)}


class DatasetListResource(Resource):
    decorators = [auth.login_required]

    def get(self):
        datasets = Dataset.query.all()
        return {'datasets': marshal([dataset for dataset in datasets], dataset_fields)}


class DatapointResource(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        datapoint = Datapoint.query.get_or_404(id)
        return {'datapoint': marshal(datapoint, datapoint_fields)}


class DatapointListResource(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        datapoints = Datapoint.query.filter_by(dataset_id=id).all()
        return {'datapoints': marshal([datapoint for datapoint in datapoints], datapoint_fields)}
