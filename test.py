from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Does before each"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure HTML is displayed"""
        with self.client:
            response = self.client.get('/')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<div class="boggle-board">', html)
            self.assertIn('<p class="high-score">High Score: ', html)
            self.assertIn('<p>Words Found!!</p>', html)

    def test_session_info(self):
        """Make sure session is working properly"""
        with app.test_client() as client:
            resp = client.get("/")
            print(session)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("board", session)
            self.assertNotIn("high_score", session)
            self.assertNotIn("high-score", session)

    def test_valid_guess(self):
        """Checks if guess is valid"""
        with self.client as client:
             with client.session_transaction() as change_session:
                change_session['board'] = [["C", "A", "R", "X", "X"], 
                                 ["X", "X", "X", "X", "X"], 
                                 ["X", "X", "X", "X", "X"], 
                                 ["X", "X", "X", "X", "X"], 
                                 ["X", "X", "X", "X", "X"]]
        response = self.client.get('/check-guess?guess=car')
        self.assertEqual(response.json['result'], 'ok')

    def test_not_a_word(self):
        """Tests a non-word"""

        self.client.get('/')
        response = self.client.get(
            '/check-guess?guess=vmakeis')
        self.assertEqual(response.json['result'], 'not-word')

    def test_not_on_board(self):
        """Tests word that is a word but not on board"""
        self.client.get('/')
        response = self.client.get('/check-guess?guess=house')
        self.assertEqual(response.json['result'], 'not-on-board')

