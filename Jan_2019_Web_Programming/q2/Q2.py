# Question 2a)

from flask import Flask, render_template, request, url_for
from flask_api import FlaskAPI, status, exceptions

chat_data = []
avatar_data = {'Finn':'static/img/Avatars/001-man.png',\
             'Han':'static/img/Avatars/005-man-3.png',\
             'Rey':'static/img/Avatars/006-gentleman.png',\
             'Luke':'static/img/Avatars/008-man-4.png',\
             'Poe':'static/img/Avatars/009-punk.png',\
             'Ben':'static/img/Avatars/022-man-5.png',\
             'Leia':'static/img/Avatars/016-woman-8.png',\
             'unknown':'static/img/Avatars/blank-avatar.png'}
displayAttributes = ""


def avatar(name):
    if name in avatar_data:
        avatar = avatar_data[name]
    else:
        avatar = avatar_data['unknown']
    return avatar

app = Flask(__name__)

@app.route("/")
@app.route("/add-chat", methods=["GET","POST"]) #Page to add data
def add():
    if request.method == "POST":
        # Increment id of chat, to show it in chronological order later/for reference
        if chat_data is False:
            chat_id = 1
        else:
            chat_id = len(chat_data) + 1
        chat = {}
        chat['id'] = chat_id
        chat['name']= request.form.get('nameInput')
        chat['status'] = request.form.get('statusInput')
        chat['message'] = request.form.get('messageInput')
        chat['avatar'] = avatar(chat['name'])
        chat_data.append(chat)
        chat_data.sort(key=lambda k: k['id'], reverse=True) # Make new chats appear on top instead
        return render_template("chat.html", chat_data=chat_data)
    
    return render_template("chat.html", chat_data=chat_data)


@app.route("/list")  #show a list of new converation that have been added so far
def show_list():
    return render_template("list.html",chat_data=chat_data)


# Question 2b)

# This function returns chat details by chat ID
def chat_repr(key):
    for chat in chat_data:
        if key == chat['id']:
            selected_chat = chat
    return str({
        'url': request.host_url.rstrip('/') + url_for('chats_detail', key=key),
        'name': selected_chat['name'],
        'status': selected_chat['status'],
        'message': selected_chat['message'],
        'avatar':selected_chat['avatar']
    }).replace("'",'"')
    
# List or create chats
@app.route("/", methods=['GET','POST'])
def chats_list():
    if request.method == 'POST':
        # Increment id of chat, to show it in chronological order later/for reference
        if chat_data is False:
            chat_id = 1
        else:
            chat_id = len(chat_data) + 1
        chat = {}
        chat['id'] = chat_id
        chat['name']= request.form.get('nameInput')
        chat['status'] = request.form.get('statusInput')
        chat['message'] = request.form.get('messageInput')
        chat['avatar'] = avatar(chat['name'])
        chat_data.append(chat)
        chat_data.sort(key=lambda k: k['id'], reverse=True) # Make new chats appear on top instead
        return chat, status.HTTP_201_CREATED
        
    # request.method == 'GET'
    chat_id_list = [chat['id'] for chat in chat_data]
    return [chat_repr(chat_id) for chat_id in chat_id_list]

# Get, update, or delete chats. (Don't think delete is needed, but why not)
@app.route("/api/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def chats_detail(key):
    chat_id_list = [chat['id'] for chat in chat_data]
    if key in chat_id_list:
        for chat in chat_data:
            if key == chat['id']:
                selected_chat = chat
    else:
        selected_chat = False

    if request.method == 'PUT':
        name = str(request.data.get('nameInput', ''))
        status = str(request.data.get('statusInput', ''))
        message = str(request.data.get('messageInput', ''))
        avatar = avatar(name)
        if selected_chat is not False:
            chat_data.remove(selected_chat)
        
        # This works for both update and new chats, as updated chats are deleted earlier.
        chat = {}
        chat['id'] = key
        chat['name']= name
        chat['status'] = status
        chat['message'] = message
        chat['avatar'] = avatar
        chat_data.append(chat)
        chat_data.sort(key=lambda k: k['id'], reverse=True)
        return chat_repr(key)

    elif request.method == 'DELETE':
        if selected_chat is not False:
            chat_data.remove(selected_chat)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in chat_id_list:
        raise exceptions.NotFound()
    return chat_repr(key)

# Question 2c)
@app.route("/display-change")
def show_display_changes():
    displayAttributes = '''
    //Question 2c) - This page is set to be permanently formatted.
    $(document).ready(function() {
    //Question 2c) - This page is set to be permanently formatted.
        $(".recent-conversations").find("h1").css("font-weight","bold");
        $(".recent-conversations").find(".status").css("color","blue");
        //Change even numbered items in list - jQuery is 0 indexed.
        $(".recent-conversations").find("p:odd").css("color","LightGreen");
    });
    ''' # Storing display attributes in a variable in the model
    return render_template("chat.html", chat_data=chat_data, buttonScript=displayAttributes)
        
if __name__ == "__main__":
    app.run(debug=True)