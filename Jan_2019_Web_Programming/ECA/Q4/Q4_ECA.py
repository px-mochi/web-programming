from flask import Flask, render_template, redirect, request, url_for, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime

conn = sqlite3.connect('sitedata.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS users')
cur.execute('DROP TABLE IF EXISTS videos')
print('---------- Program restarted, existing tables dropped -----------') #debug
db = SQLAlchemy()
UPLOAD_FOLDER_VIDEO = 'static/img/videos'
ALLOWED_EXTENSIONS = set(['webm','ogg','mp4'])
UPLOAD_FOLDER_AVATAR = 'static/img/avatars'

# Question 2a) Keep information about banner advertisements
adBannerData = [] # A list of dicts is used as there is a limited amount of ads, and I won't be adding more ads so it is sufficient.



def start_flask():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.db'
    app.config['SECRET_KEY'] = 'Key239ECAL0ck'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_VIDEO
    #app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Max upload size of 50MB
    '''Note : App.config['MAX_CONTENT_LENGTH'] is the best way to handle too large video
    sizes, but it doesn't return the http response correctly in dev servers (Which is what
    this ECA will probabaly be run,tested, and marked on). Thus, it is not implemented here.
    
    Edit: Just noticed that the wording in the ECA meant TOTAL for one USER, not one VIDEO. 
    Doing client-side validation instead to implement.'''
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
        latestVideos = Video.query.order_by(Video.videoid.desc()).limit(5).all() #Limit changed to 5 to trigger 'view all videos', changing list to 4 in flask.
        #print(type(latestVideos[0])) #Debugging
        if current_user.is_authenticated:
            return render_template('video.html',title='Home Page',banners=adBannerData,videos=latestVideos)
        else:
            return render_template('video-notLoggedIn.html',title='Home Page',banners=adBannerData,videos=latestVideos)
    
    @main.route("/all-videos")
    def index_all():
        latestVideos = Video.query.order_by(Video.videoid.desc()).all()
        if current_user.is_authenticated:
            return render_template('video-all.html',title='All videos',banners=adBannerData,videos=latestVideos)
        else:
            return render_template('video-notLoggedIn-all.html',title='All videos',banners=adBannerData,videos=latestVideos)
    
    
    
    auth = Blueprint('auth', __name__)
    @auth.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))  #I actually have no idea, because my registration form is logging me in somehow
        return render_template('login.html',title='Login',banners=adBannerData)

    @auth.route('/login', methods=['POST'])
    def login_post():
        print('--------login_post (route /login) ----------') #debug
        # There's an inconsistent issue with flask, where any user added into the DB will be considered as authenticated even without calling login_user.
        if current_user.is_authenticated:  # You shouldn't even see the login link when actually logged in, anyway. Prevents user from accidentily accessing other accounts.
            logout_user()        
        
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
                # Well.. There's an active_user function in flask-login, but not going to do that for now
                flash('Your account has been locked due to suspicious activity.','error')
                return redirect(url_for('auth.login'))
                    
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
        print(current_user.is_authenticated)  # Online sources seem to say that flask automatically authenicates any user instance.. 
        # I SO DID NOT CALL LOGIN_USER YET, HOW DOES THIS WORK?
        
        flash('Successfully registered!','success')
        return redirect(url_for('auth.login'))
    
    @auth.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('main.index'))
    
    def storageUsed():
        for serverSpaceUsed in db.session.query(User.serverSpaceUsed).filter_by(userid=current_user.userid):
            serverSpaceUsed = serverSpaceUsed[0]
        storageLeft = serverSpaceUsed/(1024*1024)
        print(storageLeft)
        return storageLeft
    
    @main.route('/upload')
    @login_required
    def uploadVideo():
        storageLeft = "{:.2f}".format(storageUsed())
        return render_template('videoUpload.html',title='Upload Video',banners=adBannerData, storage=storageLeft)
       
    @main.route('/upload', methods=['POST'])
    @login_required
    def uploadVideo_post():
        print('------ uploadedVideo (/upload, POST)------') #debug
        videoName = request.form.get('videoNameInput')
        videoDescription = request.form.get('descriptionInput')
        #print(request.files)
        videoSize = request.content_length # This is actually not 100% accurate, as some forms don't show content_length and include other form data as well
        print('Size of video: ',videoSize) # debug
        maxVideoSize = 50 * 1024 * 1024
        storageLeft = storageUsed() * 1024 * 1024
        uploader = str(current_user.userid)
        uploadTime = datetime.today().strftime("%Y%m%d%H%M%S")
        print(uploadTime)
        
        if videoSize > maxVideoSize:
            flash('Your file is too big! Please keep your upload size to below 50mb.','error')
            return redirect(request.url)
        
        if 'videoUpload' not in request.files:
            flash('No file part','error')
            return redirect(request.url)
        file = request.files['videoUpload']
                
        if file.filename == '':  # User did not select file
            flash('Please select a video file to upload.','error')
            return redirect(request.url)
        if file and allowed_file(file.filename) and videoSize <= storageLeft: # File exists, and is an allowed type
            filename = secure_filename(file.filename)
            #print(app.config['UPLOAD_FOLDER'])
            uploadDirectory = os.path.join(app.config['UPLOAD_FOLDER'], uploader)
            if not os.path.exists(uploadDirectory):
                os.makedirs(uploadDirectory)
            uploadPath = os.path.join(uploadDirectory,uploadTime+"-"+filename)
            file.save(uploadPath)
            print("Video successfully saved in - ", uploadPath) #debug
            videoType = file.content_type
            videoUploader = current_user.email
            new_video = Video(videoName=videoName, videoDescription=videoDescription, videoPath=uploadPath,\
                              videoType=videoType, videoUploader=videoUploader )
            db.session.add(new_video)
            videoSize = os.stat(uploadPath).st_size
            current_user.serverSpaceUsed = storageLeft - videoSize
            db.session.commit()
            flash('Video successfully uploaded!','success')
            return redirect(url_for('main.index'))
        
        if videoSize >= maxVideoSize:
            flash('Your file is too big! Please keep your upload size to below 50mb.','error')
            return redirect(url_for('main.uploadVideo'))
        
    @main.route('/edit-video')
    @login_required
    def editVideo():
        uploadedVideos = Video.query.filter(Video.videoUploader == current_user.email).all()
        #print('uploadedVideos - ', type(uploadedVideos))
        
        
        return render_template('video_edit.html',title='Edit uploaded videos',banners=adBannerData,\
                               videos=uploadedVideos)

    @main.route('/edit-video', methods=['POST'])
    @login_required
    def editVideo_post():
        print('------ editVideo (/edit-video, POST)------') #debug
        videoID = request.form.get('videoidInput')
        videoName = request.form.get('videoNameInput')
        videoDescription = request.form.get('descriptionInput')
        deletingVideo = request.form.get('deleteVideo')
        
        if deletingVideo:
            Video.query.filter(Video.videoid == deletingVideo).delete()
            db.session.commit()
            
            flash('Video successfully deleted.','success')
            return redirect(request.url)
        print(videoID)
        selectedVideo = Video.query.filter_by(videoid=videoID).first()
        print("TEST YO ----------------",selectedVideo)
        selectedVideo.videoName = videoName
        selectedVideo.videoDescription = videoDescription
        db.session.commit()
        
        flash('Your video details have been updated.','success')
        return redirect(request.url)
        

    @app.errorhandler(413)
    def file_too_large(error):
        flash('Your file is too big! Please keep your upload size to below 50mb.','error')
        return redirect(url_for('main.uploadVideo'))
    
    
    @main.route('/profile')
    @login_required
    def editProfile():
        return render_template('profile.html',title='Edit profile',banners=adBannerData, profile=current_user)
    
    @main.route('/profile', methods=['POST'])
    @login_required
    def editProfile_post():
        print('------ editProfile (/profile, POST)------') #debug
        name = request.form.get('nameInput')
        description = request.form.get('descriptionInput')
        file = request.files.get('updateAvatar')
        
        # User did not upload file
        if not file:
            avatar = current_user.profileImage
        
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER_AVATAR, filename))
            avatar = UPLOAD_FOLDER_AVATAR + "/" + filename
        
        current_user.profileInfo = description
        current_user.profileImage = avatar
        current_user.profileName = name
        db.session.commit()        
        
        return redirect(url_for('main.index'))
    
    @app.route('/get-views', methods=['POST'])
    def adViewData():
        adJSON = request.get_json()
        print(adJSON)
        
        adJSON_path = adJSON['path']
        adJSON_views = adJSON['views']
        for ad in adBannerData:
            if ad['path'] == adJSON_path:
                ad['views'] = adJSON_views
        
        return 'get-views route for advertisement banners'
    
    @main.route('/admin')
    @login_required
    def admin():
        if current_user.email != 'admin@streamsite.com':
            flash('You are unauthorized to view this page.','error')
            return redirect(url_for('main.index'))
        
        #videosJoined = Video.query.join(User).all()
        videosJoined = \
            db.session.execute('''
            SELECT COUNT(DISTINCT t.videoid), ROUND(((50*1024*1024)-t.serverSpaceUsed)/(1024*1024),2), t.profileName
            FROM
            (SELECT *
            FROM videos
            LEFT JOIN users
            WHERE videos.videoUploader = users.email) t
            GROUP BY t.profileName
                    ''')
        videoPostList = []
        storageUsedList = []
        userList = []
        for row in videosJoined:
            videoPostList.append(row[0])
            storageUsedList.append(row[1])
            userList.append(row[2])
        
        array = str({"videoPosts":videoPostList,\
             "storageUsed":storageUsedList,\
             "user":userList})
        return render_template('admin.html',title='Admin dashboard', array=array )
  
    
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
    serverSpaceUsed = db.Column(db.Float)

    def __init__(self, email, password, profileInfo='This user has not added profile information.',\
                  profileName=None, profileImage='static/img/avatars/blank-avatar.png',\
                   loginAttempts=0, serverSpaceUsed=50*1024*1024):
        self.email = email
        self.password = password
        self.profileInfo = profileInfo
        self.profileImage = profileImage
        if profileName is None:
            self.profileName = email
        else:
            self.profileName = profileName
        self.loginAttempts = loginAttempts
        self.serverSpaceUsed = serverSpaceUsed
        
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
    testing_password = generate_password_hash('testing1', method='sha256')
    admin_password = generate_password_hash('password', method='sha256')
    adBannerData.append({'path':'static/img/adverts/banner1.png','views':0})
    adBannerData.append({'path':'static/img/adverts/banner2.png','views':0})
    
    with app.app_context(): #add data into database in the content of the app
        db.session.add_all([
            # Due to client and server side restrictions, admins have to also log in via email.
            User(email='admin@streamsite.com',password=admin_password,\
                 profileInfo='Admins log in via email as well due to client and server side validations on login emails. Visit /admin for more info about your site.',\
                 profileImage='static/img/avatars/blank-avatar.png',profileName='Admin'),
            User(email='Lily@test.com',password=testing_password,\
                 profileInfo='Hi guys rememmber to like share and subscribe and hit dat bell button for updates',\
                 profileImage='static/img/avatars/014-woman-6.png',profileName='Lily'),
            User(email='Rachel@test.com',password=testing_password,\
                 profileInfo='Welcome to my cooking livesteam!',\
                 profileImage='static/img/avatars/016-woman-8.png',profileName='Rachel'),
            User(email='Tom@test.com',password=testing_password,\
                 profileInfo='Like my orange hair? Or hairstyle?',\
                 profileImage='static/img/avatars/009-punk.png',profileName='Tom'),
            User(email='ProfileFour@test.com',password=testing_password,\
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

def allowed_file(filename):
    allowedExtension = '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
    return allowedExtension

if __name__ == "__main__":
    app = start_flask()
    db.create_all(app=app)
    load_data(app)
    app.run(debug=True)