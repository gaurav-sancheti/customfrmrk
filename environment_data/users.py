import logging


class AbstractUser:
    def __init__(self):
        self.username = None
        self.email_address = None
        self.password = None
        self.display_name = None
        self.openid_uuid = None
        self.company_id = None
        self.company_name = None
        self.language_code = None


class PlatformUser(AbstractUser):
    def __init__(self, env_data=None, user_ref=None):
        super().__init__()
        self.logger = logging.getLogger("instr.log").getChild(__name__)
        self.env_data = env_data

        try:
            env_data['users'][user_ref]
        except KeyError:
            self.logger.info("User could not get retrieved from env_data")
            raise

        self.username = env_data['users'][user_ref].get('username')
        self.preferred_username = env_data['users'][user_ref].get('preferred_username')
        self.email_address = env_data['users'][user_ref].get('email_address') if env_data['users'][user_ref].get(
            'email_address') is not None else \
            env_data['users'][user_ref].get('username')
        self.email_verified = env_data['users'][user_ref].get('email_verified')
        self.password = env_data['users'][user_ref].get('password')
        self.passwordless = False
        self.display_name = env_data['users'][user_ref].get('display_name') if env_data['users'][user_ref].get(
            'display_name') is not None else env_data['users'][user_ref].get('name') if env_data['users'][user_ref].get(
            'name') is not None else env_data['users'][user_ref].get('username')
        self.first_name = env_data['users'][user_ref].get('first_name') if env_data['users'][user_ref].get(
            'first_name') is not None else "Test"
        self.last_name = env_data['users'][user_ref].get('last_name') if env_data['users'][user_ref].get(
            'last_name') is not None else "User"
        self.openid = env_data['users'][user_ref].get('openid')
        self.openid_uuid = env_data['users'][user_ref].get('openid_uuid')
        self.company_id = env_data['users'][user_ref].get('company_id')
        self.company_name = env_data['users'][user_ref].get('company_name')
        self.profile = env_data['users'][user_ref].get('profile')
        self.picture = env_data['users'][user_ref].get('picture')
        self.avatar_thumbnail_url = env_data['users'][user_ref].get('avatar_thumbnail_url')
        self.apikey = env_data['users'][user_ref].get('apikey')
        self.language_code = env_data['users'][user_ref].get('language_code')
