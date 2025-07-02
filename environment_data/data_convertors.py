import datetime
from base64 import b64encode


def convert_datetime_string_to_datetime(date):
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    strp_time = datetime.datetime.strptime(date, date_format)
    return strp_time


def convert_string_to_base64_encoded_string(string):
    return b64encode(bytes(string, 'utf-8')).decode('utf-8')


def convert_file_from_location_to_base64_encoded_string(image_location):
    with open(image_location, "rb") as image_file:
        image_as_base64_encoded_string = b64encode(image_file.read()).decode('utf-8')
    return image_as_base64_encoded_string
