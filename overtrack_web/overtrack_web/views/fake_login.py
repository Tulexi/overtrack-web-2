import logging

from flask import Blueprint

logger = logging.getLogger(__name__)

fake_login_blueprint = Blueprint('fake_login', __name__)


@fake_login_blueprint.route('/')
def fake_login():
    from flask import request
    from urllib import parse
    from overtrack_models.orm.user import User
    from overtrack_web.lib.authentication import make_cookie
    from flask import Response

    base_hostname = parse.urlsplit(request.base_url).hostname
    if base_hostname not in ['127.0.0.1', 'localhost']:
        logging.error('/fake_login exposed on non-loopback device: FLASK_DEBUG should not be set on nonlocal deployments')
        return f'Refusing to serve /fake_login on nonlocal base URL: {base_hostname}', 403
    else:
        if 'username' in request.args:
            try:
                user = User.username_index.get(request.args['username'])
            except User.DoesNotExist:
                return 'User does not exist', 404
            else:
                resp = Response(f'You are now authenticated as {user.username}')
                resp.set_cookie(
                    'session',
                    make_cookie(user)
                )
                return resp
        else:
            return 'Please specify a username to authenticate as. Use ?username=...', 400