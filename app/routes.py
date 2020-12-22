from flask import render_template
from app import app, db
from app.forms import LoginForm, IpAddForm, SearchForm, UserAddForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from app.models import User, Ipinfo
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from flask_login import login_required

from flask import jsonify
import json
from flask import g
from flask import current_app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    ipinfos = Ipinfo.query.order_by(Ipinfo.ip.asc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=ipinfos.next_num) \
        if ipinfos.has_next else None
    prev_url = url_for('index', page=ipinfos.prev_num) \
        if ipinfos.has_prev else None
    return render_template("index.html", title='Home Page', ipinfos=ipinfos.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route('/user_manager', methods=['GET', 'POST'])
def user_manager():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.username.asc()).paginate(
        page, app.config['USERS_PER_PAGE'], False)
    next_url = url_for('user_manager', page=users.next_num) \
        if users.has_next else None
    prev_url = url_for('user_manager', page=users.prev_num) \
        if users.has_prev else None
    return render_template("user_manager.html", title='Home Page', users=users.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/user_add', methods=['GET', 'POST'])
@login_required
def user_add():
    form = UserAddForm(role=2)
    if form.validate_on_submit():
        user_exist = User.query.filter_by(username=form.username.data).first()
        if user_exist is not None:
            flash(('The username has been used. Please use a different username.'))
            return render_template("user_add.html", title='Home Page', form=form)
        user = User(username=form.username.data, role=dict(form.role.choices).get(form.role.data))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(('Congratulations, you have add a user!'))
        return redirect(url_for('user_manager'))
    return render_template("user_add.html", title='Home Page', form=form)


@app.route('/getUserById',methods=['POST'])
@login_required
def getUserById():
    id = request.form['id'] 
    user = User.query.get(id)      
    username = user.username
    random_str = 'canyouguessit?'
    role = user.role
    if role == 'admin':
        role_id = 1
    else:
        role_id = 2
    ip_result = []
    ip_result.append({'username':username,'role_id':role_id, 'password':random_str})
    return json.dumps(ip_result)


@app.route('/updateUser', methods=['POST'])
@login_required
def updateUser():
    id = request.form['id']
    user = User.query.get(id)
    username_req = request.form['username']
    if user.username != username_req:
        user_exist = User.query.filter_by(username=username_req).first()
        if user_exist is not None:
            return json.dumps({'status':'The username has been used. Please use a different username.'})
        else:
            user.username = request.form['username']    
    role_id = request.form['role_id']
    password = request.form['password']
    if password !=  'canyouguessit?':
        user.set_password(password)
    if role_id == '1':
        user.role = 'admin'
    else:
        user.role = 'general_user'
    db.session.add(user)
    db.session.commit()
    flash(('Congratulations, you have modify the user information!'))
    return json.dumps({'status':'OK'})


@app.route('/deleteUser', methods=['POST'])
@login_required
def user_delete():
    id = request.form['id']
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()    
    return json.dumps({'status':'OK'})


@app.route('/ip_add', methods=['GET', 'POST'])
@login_required
def ip_add():
    form = IpAddForm()
    if form.validate_on_submit():
        ip_exist = Ipinfo.query.filter_by(ip=form.ip.data).first()
        if ip_exist is not None:
            flash(('The ip exists. Please use a different ip.'))
            return render_template("user_ip_add", title='Home Page', form=form)
        ipinfo = Ipinfo(ip=form.ip.data, hostname=form.hostname.data, device_type=form.device_type.data, \
            user=form.user.data, project=form.project.data)
        db.session.add(ipinfo)
        db.session.commit()
        flash(('Congratulations, you have modify the ip information!'))
        return redirect(url_for('index'))
    return render_template("ip_add.html", form=form)


@app.route('/getIpinfoById',methods=['POST'])
@login_required
def getIpinfoById():
    id = request.form['id'] 
    ipinfo = Ipinfo.query.get(id)      
    ip = ipinfo.ip
    hostname = ipinfo.hostname
    device_type = ipinfo.device_type
    user = ipinfo.user
    project = ipinfo.project
    ip_result = []
    ip_result.append({'ip':ip,'hostname':hostname,'device_type':device_type, 'user':user, 'project':project})
    return json.dumps(ip_result)


@app.route('/updateIpinfo', methods=['POST'])
@login_required
def updateIpinfo():
    id = request.form['id']
    new_ipinfo = Ipinfo.query.get(id)
    ip_req = request.form['ip']
    if new_ipinfo.ip != ip_req:
        ip_exist = Ipinfo.query.filter_by(ip=ip_req).first()
        if ip_exist is not None:
            return json.dumps({'status':'The ip exists. Please use a different ip.'})
        else:
            new_ipinfo.ip = request.form['ip']   
    new_ipinfo.hostname = request.form['hostname']
    new_ipinfo.device_type = request.form['device_type']
    new_ipinfo.user = request.form['user']
    new_ipinfo.project = request.form['project']
    db.session.add(new_ipinfo)
    db.session.commit()
    flash(('Congratulations, you have modify the ip information!'))
    return json.dumps({'status':'OK'})

@app.route('/deleteIpinfo', methods=['POST'])
@login_required
def ip_delete():
    id = request.form['id']
    ipinfo = Ipinfo.query.get(id)
    db.session.delete(ipinfo)
    db.session.commit()    
    return json.dumps({'status':'OK'})


@app.before_request
def before_request():
    if current_user.is_authenticated:       
        g.search_form = SearchForm()

@app.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    ipinfos, total = Ipinfo.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', ipinfos=ipinfos,
                           next_url=next_url, prev_url=prev_url)
