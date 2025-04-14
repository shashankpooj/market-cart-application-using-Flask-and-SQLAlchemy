from mart import app
from mart import db
from flask import render_template,redirect,url_for,flash,request
from mart.models import Item,User
from mart.forms import RegisterForm,LoginForm,PurchaseItemForm
from flask_login import login_user,logout_user,login_required,current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

from flask import session

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()

    # Initialize a session key to track purchased items in this session
    if 'purchased_items' not in session:
        session['purchased_items'] = []

    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()

        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy
                p_item_object.owner = current_user.id
                current_user.budget -= p_item_object.price
                db.session.commit()

                # ✅ Track purchased item in session
                purchased = session['purchased_items']
                purchased.append(p_item_object.id)
                session['purchased_items'] = purchased

                flash(f"Item purchased successfully and added to your cart: {p_item_object.name}", category='success')
            else:
                flash(f"Unfortunately, you do not have enough funds to purchase {p_item_object.name}.", category='danger')

        return redirect(url_for('market_page'))

    # ✅ Get all items and filter out the ones purchased in this session
    all_items = Item.query.all()
    purchased_ids = session.get('purchased_items', [])
    items_to_show = [item for item in all_items if item.id not in purchased_ids]

    return render_template('market.html', items=items_to_show, purchase_form=purchase_form)






    # Query items that are available (owner is None) and not owned by the current user
    


  

from flask import redirect, url_for

@app.route('/delete/<int:id>')
def delete_item(id):
    item_to_delete = Item.query.get_or_404(id)  # Get item or return 404 if not found
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('market_page'))

@app.route('/register',methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}',category='danger')
    return render_template('register.html',form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/session_history')
@login_required
def session_history():
    purchased_ids = session.get('purchased_items', [])
    purchased_items = Item.query.filter(Item.id.in_(purchased_ids)).all()
    return render_template('session_history.html', items=purchased_items)

