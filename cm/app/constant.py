
CELERY_BROKER_URL_DOCKER = 'amqp://admin:mypass@rabbit:5672/'
CELERY_BROKER_URL_LOCAL = 'amqp://localhost/'


CM_REGISTER_Q = 'rpc_queue_CM_register' # Do no change this value

CM_NAME = 'CM - Vehicle stock at NUTS 2 level'
RPC_CM_ALIVE= 'rpc_queue_CM_ALIVE' # Do no change this value
RPC_Q = 'rpc_queue_CM_compute' # Do no change this value
CM_ID = 16 # CM_ID is defined by the enegy research center of Martigny (CREM)
PORT_LOCAL = int('500' + str(CM_ID))
PORT_DOCKER = 80

#TODO ********************setup this URL depending on which version you are running***************************

CELERY_BROKER_URL = CELERY_BROKER_URL_DOCKER
PORT = PORT_DOCKER

#TODO ********************setup this URL depending on which version you are running***************************

TRANFER_PROTOCOLE ='http://'

INPUTS_CALCULATION_MODULE = [

    {'input_name': 'Distance traveled per vehicle and year',
     'input_type': 'input',
     'input_parameter_name': 'kmperyear',
     'input_value': 11000,
     'input_unit': 'km/year',
     'input_min': 7000,
     'input_max': 15000,
     'cm_id': CM_ID
     },
    {'input_name': 'Share electric vehicle on stock (2030)',
     'input_type': 'input',
     'input_parameter_name': 'share_vehicles',
     'input_value': 30,
     'input_unit': '%',
     'input_min': 0,
     'input_max': 100,
     'cm_id': CM_ID
     },
    {'input_name': 'Electricity consumption per 100km ',
     'input_type': 'input',
     'input_parameter_name': 'energy_per_100km',
     'input_value': 17,
     'input_unit': '%',
     'input_min': 12,
     'input_max': 25,
     'cm_id': CM_ID
     }
    
]

SIGNATURE = {

    "category": "Demand",
    "cm_name": CM_NAME,
    "authorized_scale":["NUTS 2"],
    "layers_needed": [],
    "type_layer_needed": [
        {"type": "nuts_id_number", "description": "A default layer is used here."}
    ],
    "cm_url": "Do not add something",
    "cm_description": "This calculation module interpolates the values of vehicle stock at NUTS 0 under BaU scenario into NUTS 2 level. We suggest to look into each NUTS 2 level separately, as the data are available for different time periods depending on the region and aggregating them may not lead to a meaningful result.",
    "cm_id": CM_ID,
    "wiki_url": "https://wiki.hotmaps.hevs.ch/en/CM-Vehicle-stock-at-NUTS-2-level", 
    'inputs_calculation_module': INPUTS_CALCULATION_MODULE
}
