#!/usr/bin/env python
"""
tests
"""
import codetest
import json
import unittest


class CrudTestCase(unittest.TestCase):
    def setUp(self):
        codetest.app.config['TESTING'] = True
        self.app = codetest.app.test_client()

    def test_crud(self):
        # Create a new user
        response = self.app.post('/users',
                                 data={'first_name': 'Allan',
                                       'last_name': 'Adair',
                                       'userid': 'aadair',
                                       'groups': ['users']},
                                 follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200

        # Try to create a user that already exists, expect 400 error
        response = self.app.post('/users',
                                 data={'first_name': 'Allan',
                                       'last_name': 'Adair',
                                       'userid': 'aadair',
                                       'groups': ['users']},
                                 follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 400

        # Update a user that doesn't exist, expect a 404 error
        response = self.app.put('/users/nobody',
                                data={'first_name': 'nobody',
                                      'last_name': 'knows',
                                      'userid': 'nknows',
                                      'groups': ['unkown']},
                                follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 404

        # Delete a user that doesn't exist, expect 404 error
        response = self.app.delete('/users/nobody', follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 404

        # Get the previously created user
        response = self.app.get('/users/aadair', follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200

        # Update the user with a new group
        response = self.app.put('/users/aadair',
                                data={'first_name': 'Allan',
                                      'last_name': 'Adair',
                                      'userid': 'aadair',
                                      'groups': ['admin', 'users']},
                                follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200

        # Get the user, and check for new group
        response = self.app.get('/users/aadair', follow_redirects=True)
        user = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200
        assert 'admin' in user.get('groups')

        # Delete the user
        response = self.app.delete('/users/aadair', follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200

        # Make sure user is deleted, expect 404 error
        response = self.app.get('/users/aadair', follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 404

        # Create a new group
        response = self.app.post('/groups',
                                 data={'name': 'blah'},
                                 follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200

        # Try to create a group that already exists, expect 400 error
        response = self.app.post('/groups',
                                 data={'name': 'blah'},
                                 follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 400

        # Update a group that doesn't exist, expect a 404 error
        response = self.app.put('/groups/unknown',
                                data={'members': ['aadair']},
                                follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 404

        # Delete a user that doesn't exist, expect 404 error
        response = self.app.delete('/groups/unknown', follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 404

        # Get members of new group (should be empty)
        response = self.app.get('/groups/blah', follow_redirects=True)
        assert response.status_code == 200

        # Add member to a group
        response = self.app.put('/groups/blah',
                                data={'members': ['aadair']},
                                follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200

        # Get the group, and check for added member
        response = self.app.get('/groups/blah', follow_redirects=True)
        group = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200
        assert 'aadair' in group.get('members')

        # Delete the group
        response = self.app.delete('/groups/blah', follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200

        # Make sure group is deleted, expect 404 error
        response = self.app.get('/groups/blah', follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 404

if __name__ == '__main__':
    unittest.main()
