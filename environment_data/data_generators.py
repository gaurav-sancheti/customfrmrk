import string
import uuid
from random import choice


def generate_random_email_address(email_domain=None, lower_case_only=False):
    email_domain = email_domain if email_domain is not None else generate_random_string_of_letters(16) + '.test'
    email_address = 'apithon.' + generate_random_string_of_letters(10) + '@' + email_domain

    if lower_case_only is True:
        email_address = email_address.lower()
    else:
        while not (any(_.isupper() for _ in email_address) and any(_.islower() for _ in email_address)):
            email_address = f"apithon.{generate_random_string_of_letters(10)}@{email_domain}"
        else:
            pass

    return email_address


def generate_random_email_domain(email_domain=None, lower_case_only=False):
    email_domain = email_domain if email_domain is not None else generate_random_string_of_letters(16) + '.test'
    return email_domain.lower() if lower_case_only is True else email_domain


def generate_random_string_of_letters(length):
    return "".join(choice(string.ascii_letters) for _ in range(length))


def generate_uuid():
    return str(uuid.uuid4())
