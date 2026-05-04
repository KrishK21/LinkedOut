## Mustaph Mohamed
# BBelow is my test file for the auth.py file testing my sign up, login and the profile functions I wrote.
# I have both black box and white box unit tests in this file as well as an integration test.
# I have 19 assertions in total in this test file.
# I have a test database that I use for testing and I make sure to delete it after every test so that I start fresh for every test.
# I also make sure to create the upload folder if it does not exist because I have a test that uploads a resume and I need to make sure that the folder is there for the test to pass.
# All my tests passed after some modifications and playing around with the original login and signup functions i made couple weeks ago.
# Github should now have the most up to date version of the auth.py file and the db.py file as well as this test file and also cleaned up the repository
# The repo is now organized and files are placed within folders either frontend or backend depending on what the coding is doing.
# All the test I have passed annd python's built in unnittest framework is being used to run the tests in the terminal.


import unittest
import os
import sqlite3
from auth import app, UPLOAD_FOLDER


class AuthTestCase(unittest.TestCase):
    testUns = "testuser"
    testPWs = "testpass"
    TEST_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "test.db")

    @classmethod
    def setUpClass(cls):
        # This will point to the test db.
        app.config["TESTING"] = True
        app.config["DATABASE"] = cls.TEST_DB

        # First we have to make sure that the folder exist becan we can upload it. 
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    def setUp(self):
        # This handles the creation of the test client.
        self.client = app.test_client()

        # This handles the intialization of the test db.
        self.init_db()

    def tearDown(self):
        # We have to remove the test db after every time we test.
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)

    def init_db(self):
        conn = sqlite3.connect(self.TEST_DB)
        c = conn.cursor()
        # This handles the dropping of the tables if they exist so that we start new for every test.
        c.execute("DROP TABLE IF EXISTS users")
        c.execute("DROP TABLE IF EXISTS profiles")
        conn.commit()
        conn.close()

# Below is the black box unit tests section. 
# This is a black boc unit test
# Under the unit signup route
# This specificaally handles the case we have empty fields in the signup route.
    def testEmpty(self): 
        resp = self.client.post('/signup', json={"username": "", "password": self.testPWs})
        self.assertEqual(resp.status_code, 400) # This assertion 1.
        data = resp.get_json()
        self.assertIn("error", data) # This is assertion 2.
        resp = self.client.post('/signup', json={"username": self.testUns, "password": ""})
        self.assertEqual(resp.status_code, 400) # This is assertion 3.
        data = resp.get_json()
        self.assertIn("error", data) # This is assertion 4.

# This is a black box unit test
# Under the unit signup route
# This specifically handles the case we have a valid signup and we get a user id back.
    def testSignup(self):
        resp = self.client.post('/signup', json={"username": self.testUns, "password": self.testPWs})
        self.assertEqual(resp.status_code, 201) # This is assertion 5.
        data = resp.get_json()
        self.assertIn("user_id", data) # This is assertion 6.

# This is a black box unit test
# Under the unit signup route
# This specifically handles the case we have a duplicate username.
    def testSignupDup(self):
        # First signup
        self.client.post('/signup', json={"username": self.testUns, "password": self.testPWs})
        # Second signup
        resp = self.client.post('/signup', json={"username": self.testUns, "password": self.testPWs})
        self.assertEqual(resp.status_code, 400) # This is assertion 7
        data = resp.get_json()
        self.assertIn("error", data) # This is assertion 8


# This is the White box unit tests
# Under the unit login route
    def testLogin(self):
        # We first have to sign up the user and create their account.
        self.client.post('/signup', json={"username": self.testUns, "password": self.testPWs})
        #After we create the user's account then we can test the login route with the right credentials we just created.
        resp = self.client.post('/login', json={"username": self.testUns, "password": self.testPWs})
        self.assertEqual(resp.status_code, 200)  # This is assertion 9
        data = resp.get_json()
        self.assertIn("message", data) # This is assertion 10



# This is the white box unit tests sections. Below is the function we are testing, the login function.
#@app.route("/login", methods=["POST"])
#def login():
    ##data = request.get_json() or {}
    #username = data.get("username", "").strip()
    #password = data.get("password", "").strip()
    #if not username or not password:
        #return jsonify({"error": "Please enter password and username."}), 400
    #try:
        #db = get_db()
        #db.execute("""
            #CREATE TABLE IF NOT EXISTS users (
                #id INTEGER PRIMARY KEY AUTOINCREMENT,
                #username TEXT UNIQUE NOT NULL,
                #password_hash TEXT NOT NULL
            #)
        #""")
        #user = db.execute(
            #"SELECT * FROM users WHERE username = ?", (username,)
        #).fetchone()
        ##if user is None:
            #return jsonify({"error": "Invalid credentials"}), 401
        #if not check_password_hash(user["password_hash"], password):
            #return jsonify({"error": "Invalid credentials"}), 401
        #return jsonify({
            #"message": "Login was successful",
            #"user_id": user["id"],
            #"username": user["username"]
        #}), 200
    #except Exception as e:
        #return jsonify({"error": f"Error while in login route: {str(e)}"}), 400
    
# This is a white box unit test
# Under the unit login route
# This specifically handles the case we have empty fields in the login route.
    def testLoginEmpty(self):
        resp = self.client.post('/login', json={"username": "", "password": self.testPWs})
        self.assertEqual(resp.status_code, 400) # This is assertion 11


# This is a white box unit test
# Under the unit login route
# This specifically handles the case we get an invalid credentials in the login route.
    def testInvalidity(self):
        resp = self.client.post('/login', json={"username": "wronguser", "password": "wrongpass"})
        self.assertEqual(resp.status_code, 401) # This is assertion 12
        data = resp.get_json()
        self.assertIn("error", data)   # This is assertion 13


# This is a white box unit test
# Under the unit login route
# This specifically handles the case we get an invalid password in the login route.
    def testWrongPW(self):
        self.client.post('/signup', json={"username": self.testUns, "password": self.testPWs})
        resp = self.client.post('/login', json={"username": self.testUns, "password": "wrongpass"})
        self.assertEqual(resp.status_code, 401) # This is assertion 14


# This is the integration test
# We test whether the user who signed up recently can create and get their profile.
# Under the unit profile route and the signup route
# This handles when a new user creates a profile and then we can get the profile information back.
    def testProfile(self):
        signup_resp = self.client.post('/signup', json={"username": self.testUns, "password": self.testPWs})
        user_id = signup_resp.get_json()["user_id"]
        # First we create an account.
        resp = self.client.post('/profile', data={
            "user_id": user_id,
            "name": "Test User",
            "bio": "This is a test bio"
        })
        self.assertEqual(resp.status_code, 200)  # This is assertion 15
        data = resp.get_json()
        self.assertIn("message", data)  # This is assertion 16
        # Once the account is created we have to fetch the profile and check if the data is correct.
        resp = self.client.get(f'/profile?user_id={user_id}')
        self.assertEqual(resp.status_code, 200)  # This is assertion 17
        data = resp.get_json()
        self.assertEqual(data["name"], "Test User")  # This is assertion 18
        self.assertEqual(data["bio"], "This is a test bio")  # This is assertion 19

if __name__ == "__main__":
    unittest.main()