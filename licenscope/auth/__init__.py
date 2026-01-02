from licenscope.auth.basic import BasicAuth
from licenscope.auth.token import TokenAuth


AUTH_PROVIDERS = {
    BasicAuth.name: BasicAuth,
    TokenAuth.name: TokenAuth,
}
