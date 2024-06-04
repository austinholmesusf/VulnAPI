import os

project_folder = os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           os.pardir)), os.pardir))

DATABASE_NAME = 'VulnDB'
DATABASE_SCHEMA = project_folder + os.path.sep + 'schema.sql'
SECRET = '877e3401-8b72-4caf-ac7b-3f828c6b4987a19f2a72-e11a-42f4-adc4-65db302e95ea'
TOKEN_DURATION_HOURS = 24
