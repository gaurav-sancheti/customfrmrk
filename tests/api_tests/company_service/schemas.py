from schema import And, Optional, Or, Schema

from environment_data.data_validators import validate_url, validate_uuid4

post_company_full_success_response = Schema(
    {
        "companyId": Or(validate_uuid4, And(str, lambda s: len(s.strip()) > 0)),
        "name": And(str, lambda s: len(s.strip()) > 0),
        "description": Or(None, And(str, lambda s: len(s.strip()) > 0)),
        "createdAt": And(str, lambda s: len(s.strip()) > 0),
        "modifiedAt": And(str, lambda s: len(s.strip()) > 0),
        "emailDomains": [
            {
                "domain": And(str, lambda s: len(s.strip()) > 0)
            }
        ]
    }
)

post_company_partial_success_response = Schema(
    {
        "companyId": Or(validate_uuid4, And(str, lambda s: len(s.strip()) > 0)),
        "name": And(str, lambda s: len(s.strip()) > 0),
        "description": Or(None, And(str, lambda s: len(s.strip()) > 0)),
        "createdAt": And(str, lambda s: len(s.strip()) > 0),
        "modifiedAt": And(str, lambda s: len(s.strip()) > 0),
        "emailDomains": [
            {
                "name": str,
                "code": int,
                Optional("reason"): And(str, lambda s: len(s.strip()) > 0)
            }
        ]
    }
)

post_email_domains_full_success_response = Schema(
    [
        {
            "domain": And(str, lambda s: len(s.strip()) > 0)
        }
    ]
)

post_email_domains_partial_success_response = Schema(
    {
        "items": [
            {
                "name": str,
                "code": int,
                Optional("reason"): And(str, lambda s: len(s.strip()) > 0)
            }
        ]
    }
)

brand_response = Schema(
    {
        "logo": {
            "location": Or(None, And(str, lambda s: len(s.strip()) > 0))
        },
        "coverImage": {
            "location": Or(None, And(str, lambda s: len(s.strip()) > 0))
        }
    }
)

get_company_response = Schema(
    {
        "companyId": Or(validate_uuid4, And(str, lambda s: len(s.strip()) > 0)),
        "name": And(str, lambda s: len(s.strip()) > 0),
        "description": Or(None, And(str, lambda s: len(s.strip()) > 0)),
        "digitallySignEmails": bool,
        "logoUrl": Or(None, And(str, lambda s: len(s.strip()) > 0)),
        "createdAt": And(str, lambda s: len(s.strip()) > 0),
        "modifiedAt": And(str, lambda s: len(s.strip()) > 0)
    }
)

get_company_brand_response = Schema(
    {
       "uuid": validate_uuid4,
       "modifiedAt": And(str, lambda s: len(s.strip()) > 0),
       "assets": [
          {
             "key": And(str, lambda s: len(s.strip()) > 0),
             "location": validate_url
          }
       ]
    }
)

error_response_rfc7807 = Schema(
    {
        "status": int,
        "title": And(str, lambda s: len(s.strip()) > 0),
        "detail": And(str, lambda s: len(s.strip()) > 0)
    }
)

error_response = Schema(
    {
        "error": {
            Optional("type"): str,
            "message": And(str, lambda s: len(s.strip()) > 0),
            Optional("detail"): And(str, lambda s: len(s.strip()) > 0),
            "code": int,
            "instance": And(str, lambda s: len(s.strip()) > 0),
            Optional("invalid-params"): [
                {
                    "name": str,
                    "reason": And(str, lambda s: len(s.strip()) > 0)
                },
                {
                    "name": str,
                    "reason": And(str, lambda s: len(s.strip()) > 0)
                }

            ]
        }
    }
)

generic_error_response = Schema(
    {
        "error": {
            "code": int,
            "message": And(str, lambda s: len(s.strip()) > 0)
        }
    }
)
