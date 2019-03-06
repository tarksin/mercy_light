# mercy_light.py
from mercy_light import app, db
from flask import Flask, render_template, url_for, request, session, redirect, flash, abort
from flask_login import login_user, login_required, logout_user
from mercy_light.models import User, Nutrient  #
from mercy_light.forms import AddNutrientForm, OrganismForm, DelNutrientForm, SignupForm, LoginForm  # mercy_light.

import pymysql

# from flask_wtf import FlaskForm
# from flask_sqlalchemy import SQLAlchemy
# from wtforms import (StringField, SubmitField, IntegerField, BooleanField,
#                     DateTimeField, RadioField,SelectField, TextField, TextAreaField)
# from wtforms.validators import DataRequired
# from forms import AddNutrientForm, OrganismForm, DelNutrientForm, SignupForm, LoginForm
# from flask_bcrypt import Bcrypt

    # app = Flask(__name__)
    #
    # app.config['DEBUG'] = True      # displays runtime errors in the browser, too
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://maxx:xnynzn987@localhost:3306/nutrition'
    # app.config['SQLALCHEMY_ECHO'] = False
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SECRET_KEY'] = '84db222b-431f-4461-bef9-914b7671fb4c'
    #
    # db = SQLAlchemy(app)
#-------------------------------------------------------------------------------
# ''' nutrients =
#  id      | int(11)     | NO   | PRI | NULL              | auto_increment              |
#| n_time  | timestamp   | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
#| item    | varchar(50) | YES  |     | NULL              |                             |
#| kcal    | int(11)     | YES  |     | NULL              |                             |
#| fat     | int(11)     | YES  |     | NULL              |                             |
#| carbs   | int(11)     | YES  |     | NULL              |                             |
#| protein | int(11)     | YES  |     | NULL              |
#| user_id | int(11)     | NO  |     | NULL              |
#users  =
#id            | int(11)      | NO   | PRI | NULL    | auto_increment |
#| username      | varchar(32)  | YES  |     | NULL    |                |
#| password_hash | varchar(128) | YES  |     | NULL    |
#1 | mees64101 | asdfasdf                                                                                      |
#|  2 | xumi      | pbkdf2:sha256:50000$j62L...
#-----------------------------------------  <br>
  # {{ form.pass_confirm.label }}{{ form.pass_confirm }}
#--------------------------------------


@app.route('/')
@app.route('/index')
def vf_index():
    # return "<h2 style = 'color: maroon; font-family: ubuntu; text-align: center;'>bioinfx.org</h2><h6></h6>"
    return render_template('index.html')


@app.route('/add_nutrient', methods=['GET','POST'])
def vf_add_nutrient():
    nutrient = False;
    form = AddNutrientForm()

    if form.validate_on_submit():
        flash('Successful recording of {}'.format(form.item.data))
        # session['item'] = form.item.data session['kcal'] = form.kcal.data session['fat'] = form.fat.data
        # session['carbs'] = form.carbs.data      session['protein'] = form.protein.data
        item = form.item.data
        kcal = form.kcal.data
        fat = form.fat.data
        carbs = form.carbs.data
        protein = form.protein.data

        new_item = Nutrient(item, kcal, fat, carbs, protein, 1)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('vf_today_list'))

    return render_template('add_nutrient.html', form=form)

@app.route('/today_list' , methods=['GET','POST'])
def vf_today_list():
    nutrients = Nutrient.query.all()
    return render_template('today_list.html', nutrients = nutrients)

@app.route('/del_nutrient' , methods=['GET','POST'])
def vf_del_nutrient():

    form = DelNutrientForm()
    if form.validate_on_submit():
        id = form.id.data
        nutrient = Nutrient.query.get(id)
        db.session.delete(nutrient)
        db.session.commit()
        return redirect(url_for('vf_today_list'))
    return render_template('del_nutrient.html', form=form)


@app.route('/organism' , methods=['GET','POST'])
def vf_organism():
    organism = False;
    # organism = 'Saccharomyces cerevisiae';
    form = OrganismForm()

    if form.validate_on_submit():
        flash('Successful registration of {}'.format(form.organism.data))
        session['organism'] = form.organism.data
        session['ref_seq_ann'] = form.ref_seq_ann.data
        session['tot_seq_len'] = form.tot_seq_len.data
        session['assembly_level'] = form.assembly_level.data
        session['assembly_name'] = form.assembly_name.data
        return redirect(url_for('vf_confirm'))

    return render_template('organism.html', form=form)

          #, form=form,organism=organism)

@app.route('/welcome')
@login_required
def vf_welcome():
    return render_template('welcome.html')

@app.route('/logout')
@login_required
def vf_logout():
    logout_user()
    flash("You are logged out")
    return redirect(url_for('vf_index'))



@app.route('/confirm')
def vf_confirm():
    return render_template('confirm.html')
    # fname=request.args.get('fname')
    # lname=request.args.get('lname')
    # if len(fname) < 4:
    #     return render_template('404.html', error = "First name is too short")
    # else:

@app.route('/researchers')
def vf_researchers():
    header="bioinfx"
    researchers=["Juan Gonsalvez", "Rakhim Makim", "Julia Wolfson", "Gregor Miksa", "Andrev Mikalik"]
    return render_template("researchers.html", header=header, researchers=researchers)


@app.route('/genomics')
def vf_genomics():
    return "<h2 style = 'color: maroon; font-family: ubuntu; text-align: center;'>genomics for the curious</h2><p>{}</p>".format(__name__)

@app.route('/register', methods=['GET','POST'])
def vf_register():

    form = SignupForm()
    if form.validate_on_submit():
        flash('Successful registration of {}'.format(form.username.data))
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("Welcome to Mercy Light")
        return redirect(url_for('vf_login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET','POST'])
def vf_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in')
            next = request.args.get('next')
            if next == None or not next[0]== '/':
                next = url_for('vf_welcome')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/404')
def vf_404():
    return render_template('404.html')

@app.errorhandler(404)
def vf_page_not_found(e):
    return render_template('404.html',error=e), 404

@app.route('/thankyou')
def vf_thankyou():
    fname=request.args.get('fname')
    lname=request.args.get('lname')
    if len(fname) < 4:
        return render_template('404.html', error = "First name is too short")
    else:
        return render_template('thankyou.html', fname=fname, lname=lname)


@app.route('/researcher/<id>')
def vf_researcher(id):
    rsch=["Juan Gonsalvez", "Rakhim Makim", "Julia Wolfson", "Gregor Miksa", "Andrev Mikalik"]
    return "<h1 style = 'color: maroon; font-family: ubuntu; text-align: center;'>{}</h1>".format(rsch[int(id)] )

@app.route('/cat_latin/<name>')
def cat_latin(name):
    lat = ''
    if name[-1] == 'y':
        lat = name[:-1] + 'ify'
    else:
        lat = name + 'y'
    return "<h2 style = 'color: maroon; font-family: ubuntu; text-align: center;'>{}</h2><p></p>".format(lat)


if __name__ == "__main__":
    app.run(debug=True)
