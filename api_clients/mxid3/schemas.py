from schema import And, Schema

access_token_dict = {"sub": And(str, lambda s: len(s.strip()) > 0),
                     "aud": And(str, lambda s: len(s.strip()) > 0),
                     "nbf": And(int, lambda i: i >= 0),
                     "iss": And(str, lambda s: len(s.strip()) > 0),
                     "exp": And(int, lambda i: i >= 0),
                     "iat": And(int, lambda i: i >= 0)}

access_token = Schema(access_token_dict,
                      ignore_extra_keys=True)

access_token_payload = Schema({"access_token": And(str, lambda s: len(s.strip()) > 0),
                               "refresh_token": And(str, lambda s: len(s.strip()) > 0),
                               "scope": And(str, lambda s: len(s.strip()) > 0),
                               "id_token": And(str, lambda s: len(s.strip()) > 0),
                               "token_type": And(str, "Bearer"),
                               "expires_in": And(int, lambda i: i >= 0),
                               "nonce": And(str, lambda s: len(s.strip()) > 0),
                               "jti": And(str, lambda s: len(s.strip()) > 0)
                               })

access_token_mocked_payload = Schema({"access_token": And(str, lambda s: len(s.strip()) > 0),
                                      "scope": And(str, lambda s: len(s.strip()) > 0),
                                      "id_token": And(str, lambda s: len(s.strip()) > 0),
                                      "token_type": And(str, "Bearer"),
                                      "expires_in": And(int, lambda i: i >= 0)
                                      })
