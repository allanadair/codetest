"""
codetest module

This is a quick and dirty exercise.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)
user_store = {}
group_store = {}


@app.errorhandler(404)
def not_found(error=None):
    """
    Custom JSON error handler for not found.
    """
    # NOTE: This is a quick and dirty approach.
    message = {'message': 'Not found: {0}'.format(request.url)}
    response = jsonify(message)
    response.status_code = 404
    return response


@app.errorhandler(400)
def bad_request(error=None):
    """
    Custom JSON error handler for bad request.
    """
    # NOTE: This is a quick and dirty approach.
    message = {'message': 'Bad request: {0}'.format(request.url)}
    response = jsonify(message)
    response.status_code = 400
    return response


@app.route('/users', methods=['POST'])
@app.route('/users/<userid>', methods=['GET', 'PUT', 'DELETE'])
def users(userid=None):
    """
    CRUD operations on users.
    """
    if request.method == 'GET' and userid:
        # Returns the matching user record or 404 if the user doesn't exist.
        user = user_store.get(userid)
        if user:
            return jsonify(user)
        return not_found()

    if request.method == 'POST' and not userid:
        # Creates a new user record. The body of the request should be a valid
        # user record. POSTs to an existing user should be treated as errors
        # and flagged with the appropriate HTTP status code.
        keys = ('first_name', 'last_name', 'userid', 'groups')
        userid = request.form.get('userid')

        # True if request has expected keys.
        has_keys = all(key in request.form for key in keys)

        if has_keys and userid not in user_store:
            # Adds user to user_store.
            user_store[request.form.get('userid')] = request.form
            return jsonify({'message': 'New user {0} created'.format(userid)})
        return bad_request()

    if request.method == 'PUT' and userid:
        # Updates an existing user record. The body of the request should be a
        # valid user record. PUTs to a non-existant user should return a 404.
        keys = ('first_name', 'last_name', 'userid', 'groups')
        userid = request.form.get('userid')

        # True if request has expected keys.
        has_keys = all(key in request.form for key in keys)

        if has_keys and userid in user_store:
            # Overwrites an existing user.
            user_store[request.form.get('userid')] = request.form
            return jsonify({'message': 'User {0} updated'.format(userid)})
        return not_found()

    if request.method == 'DELETE' and userid:
        # Deletes a user record. Returns 404 if the user doesn't exist.
        if user_store.get(userid):
            del user_store[userid]
            return jsonify({'message': 'User {0} deleted'.format(userid)})
        return not_found()

    return bad_request()


@app.route('/groups', methods=['POST'])
@app.route('/groups/<grp_name>', methods=['GET', 'PUT', 'DELETE'])
def groups(grp_name=None):
    """
    CRUD operations on groups.
    """
    if request.method == 'GET' and grp_name:
        # Returns a JSON list of userids containing the members of that group.
        # Should return a 404 if the group doesn't exist.
        group = group_store.get(grp_name)
        if group is not None:
            return jsonify({'members': list(group)})
        return not_found()

    if request.method == 'POST' and not grp_name:
        # Creates an empty group. POSTs to an existing group should be treated
        # as errors and flagged with the appropriate HTTP status code. The body
        # should contain a 'name' parameter
        name = request.form.get('name')
        if name and name not in group_store:
            group_store[name] = set()
            return jsonify({'message': 'New group {0} created'.format(name)})
        return bad_request()

    if request.method == 'PUT' and grp_name:
        # Updates the membership list for the group. The body of the request
        # should be a JSON list describing the group's members.
        if grp_name in group_store:
            group_store[grp_name] = set(request.form.getlist('members'))
            return jsonify({'message': 'Group {0} updated'.format(grp_name)})
        return not_found()

    if request.method == 'DELETE' and grp_name:
        # Deletes a group.
        if group_store.get(grp_name):
            del group_store[grp_name]
            return jsonify({'message': 'Group {0} deleted'.format(grp_name)})
        return not_found()

    return bad_request()

if __name__ == '__main__':
    app.run(debug=True)
