from flask import Flask, render_template, redirect, request, url_for, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required

conn = sqlite3.connect('sitedata.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS users')
cur.execute('DROP TABLE IF EXISTS videos')
print('---------- Program restarted, existing tables dropped -----------') #debug
db = SQLAlchemy()

# Question 2a) Keep information about banner advertisements
adBannerData = [] # A list of dicts is used as there is a limited amount of ads, and I won't be adding more ads so it is sufficient.

def start_flask():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.db'
    app.config['SECRET_KEY'] = 'Key239ECAL0ck'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message_category = 'error'
    
    @login_manager.user_loader
    def load_user(userid):
        return User.query.get(int(userid))
    
    # Creating blueprints for public routes
    main = Blueprint('main', __name__)
    
    @main.route("/")
    def index():
        latestVideos = Video.query.order_by(Video.videoid.desc()).limit(4).all()
        print(type(latestVideos[0])) #Debugging
        return render_template('video.html',title='Home Page',banners=adBannerData,videos=latestVideos)
    
    
    auth = Blueprint('auth', __name__)
    @auth.route('/login')
    def login():
        return render_template('login.html',title='Login',banners=adBannerData)

    @auth.route('/login', methods=['POST'])
    def login_post():
        email = request.form.get('emailInput')
        password = request.form.get('passwordInput')
        
        userFound = User.query.filter_by(email=email).first() # check if there is an existing user
        if userFound and not check_password_hash(userFound.password, password): # User exists, password was wrong
            currentAttempts = userFound.loginAttempts
            if currentAttempts is None:
                currentAttempts = 0
            userFound.loginAttempts = currentAttempts + 1
            print("Current login attempt: ",userFound.loginAttempts) #debug
            db.session.commit()            
        
        if userFound:
            if userFound.loginAttempts > 3:
                flash('Your account has been locked due to suspicious activity.','error')
                return render_template('login.html',title='Login',banners=adBannerData)
                    
        if not userFound or not check_password_hash(userFound.password, password): 
            flash('Username or password incorrect.','error')
            return redirect(url_for('auth.login'))  

        # Login successful
        print('User has been logged in!') #debug
        login_user(userFound)
        userFound.loginAttempts = 0
        db.session.commit()
        return redirect(url_for('main.index'))

    @auth.route('/register')
    def register():
        return render_template('register.html',title='Register account',banners=adBannerData)
    
    @auth.route('/register',methods=['POST'])
    def register_post():
        email = request.form.get('emailInput')
        password = request.form.get('passwordInput')
        print('test - ',password) # debug
        
        userFound = User.query.filter_by(email=email).first() # check if there is an existing user
        if userFound:
            flash('Email already exists! Did you mean to <a href="/login">login</a> instead?','error')
            return redirect(url_for('auth.register'))
        
        
        new_user = User(email=email, password=generate_password_hash(password, method='sha256')) # Creates a new user
        db.session.add(new_user)
        db.session.commit()
        
        flash('Successfully registered!','success')
        return redirect(url_for('auth.login'))
    
    @auth.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('main.index'))
    
    # blueprint for main parts of app
    app.register_blueprint(main)
    # blueprint for login pages
    app.register_blueprint(auth)
    
    return app
# Question 2a) Saves Register Users info and User Profile Information
class User(UserMixin, db.Model):
    __tablename__ = "users"
    userid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), db.ForeignKey('videos.videoUploader'), unique=True)
    password = db.Column(db.String(16))
    profileInfo = db.Column(db.String(100))
    profileImage = db.Column(db.String(100))
    profileName = db.Column(db.String(100))
    loginAttempts = db.Column(db.Integer)

    def __init__(self, email, password, profileInfo=None, profileImage='static/img/avatars/blank-avatar.png', profileName=None, loginAttempts=0):
        self.email = email
        self.password = password
        self.profileInfo = profileInfo
        self.profileImage = profileImage
        if profileName is None:
            self.profileName = email
        self.loginAttempts = loginAttempts
    
    def get_id(self):
        return self.userid
    
    def __repr__(self):
        return "%s %s %s %s %s" % \
            (self.userid, self.email, self.password, self.profileInfo, self.profileImage)

# Question 2a) Saves Video Posts information
class Video(db.Model):
    __tablename__ = "videos"
    videoid = db.Column(db.Integer, primary_key=True)
    videoName = db.Column(db.String(100))
    videoDescription = db.Column(db.String(100))
    videoPath = db.Column(db.String(100))
    videoType = db.Column(db.String(30))
    videoUploader = db.Column(db.String(100))
    uploaderProfile = db.relationship("User")
    
    def __repr__(self):
        return "%s %s %s %s %s" % \
            (self.videoid, self.videoName, self.videoDescription, self.videoPath, self.videoUploader)


def load_data(app): #Loading initial data into database
    adBannerData.append({'path':'static/img/adverts/banner1.png','views':0})
    adBannerData.append({'path':'static/img/adverts/banner2.png','views':0})
    
    with app.app_context(): #add data into database in the content of the app
        db.session.add_all([
            User(email='Lily@test.com',password='test',\
                 profileInfo='Hi guys rememmber to like share and subscribe and hit dat bell button for updates',\
                 profileImage='static/img/avatars/014-woman-6.png',profileName='Lily'),
            User(email='Rachel@test.com',password='test',\
                 profileInfo='Welcome to my cooking livesteam!',\
                 profileImage='static/img/avatars/016-woman-8.png',profileName='Rachel'),
            User(email='Tom@test.com',password='test',\
                 profileInfo='Like my orange hair? Or hairstyle?',\
                 profileImage='static/img/avatars/009-punk.png',profileName='Tom'),
            User(email='ProfileFour@test.com',password='test',\
                 profileInfo='Yo! My name is Profile Four, also known as P4. I am known for my lack of creativity in making screen names.',\
                 profileImage='static/img/avatars/006-gentleman.png',profileName='Profile Four'),
            Video(videoName='Lady Walking',videoDescription='lady Walking - video1',\
                  videoPath='https://github.com/mengchoontan/school-239/blob/master/lady-walking.mp4?raw=true',\
                  videoType='video/mp4',videoUploader='Lily@test.com'),
            Video(videoName='Lady with phone',videoDescription='lady with phone - video2',\
                  videoPath='https://github.com/mengchoontan/school-239/blob/master/lady-with-phone.mp4?raw=true',\
                  videoType='video/mp4',videoUploader='Rachel@test.com'),
            Video(videoName='Man on bike',videoDescription='Man on bike - video3',\
                  videoPath='https://github.com/mengchoontan/school-239/blob/master/man-on-bike.mp4?raw=true',\
                  videoType='video/mp4',videoUploader='Tom@test.com'),
            Video(videoName='Man sunrise',videoDescription='Man sunrise - video4',\
                  videoPath='https://github.com/mengchoontan/school-239/blob/master/man-sunrise.mp4?raw=true',\
                  videoType='video/mp4',videoUploader='ProfileFour@test.com')      
            ])
        db.session.commit()
        print("--------- Original data has been inserted into data models ----------") # debug


if __name__ == "__main__":
    app = start_flask()
    db.create_all(app=app)
    load_data(app)
    app.run(debug=True)