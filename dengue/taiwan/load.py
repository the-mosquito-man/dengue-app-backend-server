import os

from django.contrib.gis.utils import LayerMapping

from .models import Substitute


substitute_mapping = {
    'object_id': 'OBJECTID',
    'u_id': 'UID',
    'pro_id': 'PRO_ID',
    'county_id': 'COUNTY_ID',
    'town_id': 'TOWN_ID',
    'village_id': 'VILLAGE_ID',
    'v_name': 'V_Name',
    't_name': 'T_Name',
    'c_name': 'C_Name',
    'substitute': 'Substitute',
    'mpoly': 'MULTIPOLYGON'
}

substitute_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../data', 'Village_NLSC_121_1050219.shp')
)


def run(verbose=True):
    lm = LayerMapping(
        Substitute,
        substitute_shp,
        substitute_mapping,
        transform=True,
        encoding='utf-8'
    )
    lm.save(strict=False, verbose=verbose)
