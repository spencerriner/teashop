from flask import render_template, flash, redirect
from app import app
from app import db
from app.forms import LoginForm, MenuItemEditForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Employee, MenuItem, AddOnItem

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')
@app.route('/menu')
def menu():
    item_list = MenuItem.query.all()
    return render_template('menu.html', title='Menu', item_list=item_list)
@app.route('/addonitem')
def addonitem():
    addon_list = AddOnItem.query.all()
    return render_template('addon.html', title='Menu', addon_list=addon_list)
@app.route('/mgmt')
def mgmt():
    item_list = MenuItem.query.all()
    addon_list = AddOnItem.query.all()
    return render_template('mgmt.html', title='Management', item_list=item_list, addon_list=addon_list)
@app.route('/menu/<menu_item_number>', methods=['GET', 'POST'])
@login_required
def menuitem(menu_item_number):
    form = MenuItemEditForm()
    if form.validate_on_submit():
        edit_item = MenuItem.query.filter_by(menu_item_number=menu_item_number).first()
        edit_item.item_name = form.name.data
        edit_item.price = form.price.data
        edit_item.drink_type = form.drinktype.data
        edit_item.drink_description = form.description.data
        db.session.commit()
        flash('Menu item edited successfully.')
        return redirect('/mgmt')
    item_list = MenuItem.query.all()
    menu_item = MenuItem.query.filter_by(menu_item_number=menu_item_number).first_or_404()
    return render_template('mgmtmenu.html', menu_item=menu_item, item_list=item_list, form=form)
@app.route('/addon/<add_on_number>')
@login_required
def addonitemmgmt(add_on_number):
    addon_list = AddOnItem.query.all()
    addon_item = AddOnItem.query.filter_by(add_on_number=add_on_number).first_or_404()
    return render_template('mgmtaddon.html', addon_list=addon_list, addon_item=addon_item)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(employee_id=form.username.data).first()
        if employee is None or not employee.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(employee)
        flash('Login requested for user {}'.format(
            form.username.data))
        return redirect('/index')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')
