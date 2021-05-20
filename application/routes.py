from application import app, db
from application.models import Users, Inventory, LoginForm, ItemsForm
from flask import render_template, request, redirect, url_for

@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = ""
    form = LoginForm()

    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        login = form.login.data
        register = form.register.data
        all_users = Users.query.all()
        if login == True:
            if len(username) == 0:
                error = "Please enter a valid username"
            elif len(password) == 0:
                error = "Please enter a valid password"
            else:
                if len(all_users) == 0:
                    error = "Wrong Username"
                else:
                    for i in all_users:
                        if username.lower() in i.username.lower():
                            if password == i.password:
                                if username.lower() == "admin":
                                    return redirect(url_for("admin"))
                                else:
                                    return redirect(url_for("home", username = username))
                            else:
                                error = "Wrong Password"
                                break
                        else:
                            error = "Wrong Username"
        if register == True:
            return redirect(url_for("create_user"))

    return render_template('login.html', form = form, message = error)

@app.route('/register', methods = ['GET', 'POST'])
def create_user():
    error = ""
    form = LoginForm()

    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        register = form.register.data
        all_users = Users.query.all()
        if register == True:
            if len(username) == 0:
                error = "Please enter a valid username"
            elif len(password) == 0:
                error = "Please enter a valid password"
            else:
                if len(all_users) == 0:
                    user = Users(username = username, password = password)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for("login"))
                else:
                    for i in all_users:
                        if username.lower() == i.username.lower():
                            error = "Username already exists."
                            return render_template('create.html', form = form, message = error)
                            
                    user = Users(username = username, password = password)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for("login"))
                            

    return render_template('create.html', form = form, message = error)

@app.route('/home/<username>', methods = ['GET', 'POST'])
def home(username):
    error = ""
    form = ItemsForm()
    all = Inventory.query.filter_by(user_id = username).all()

    return render_template('home.html', form = form, message = error, username = username, all = all)

@app.route('/add/<username>', methods = ['GET', 'POST'])
def add(username):
    error = ""
    form = ItemsForm()

    if request.method == 'POST':
        name = form.name.data
        add = form.add_item.data
        back = form.back.data
        stock = form.stock.data
        price = form.price.data
        for_sale = form.for_sale.data

        if add == True:
            if len(name) == 0:
                error = "Please enter an item name"

            elif isinstance(stock, int) == False:
                error = "Please enter valid stock amount"

            elif len(str(stock)) == 0 or stock < 0:
                error = "Please enter valid stock amount"

            elif isinstance(price, float) == False:
                error = "Please enter valid price"

            elif len(str(price)) == 0 or price < 0:
                error = "Please enter valid price"

            else:
                new = Inventory(name = name.capitalize(), stock = stock, price = price, for_sale = for_sale, user_id = username)
                db.session.add(new)
                db.session.commit()
                return redirect(url_for("home", username = username))
        
        if back == True:
            return redirect(url_for("home", username = username))

    return render_template('add.html', form = form, message = error, username = username)

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    error = ""
    form = LoginForm()
    all = Users.query.all()

    return render_template('admin.html', form = form, message = error, all = all)

@app.route('/update/<username>/<id>', methods = ['GET', 'POST'])
def update(id, username):
    error = ""
    form = ItemsForm()
    all = Inventory.query.filter_by(id = id).all()
    
    if request.method == 'GET':
        for i in all:
            form.name.data = i.name
            form.stock.data = i.stock
            form.price.data = i.price
            form.for_sale.data = i.for_sale

    if request.method == 'POST':
        name = form.name.data
        update = form.update.data
        delete = form.delete.data
        back = form.back.data
        stock = form.stock.data
        price = form.price.data
        for_sale = form.for_sale.data

        if update == True:
            if len(name) == 0:
                error = "Please enter an item name"

            elif isinstance(stock, int) == False:
                error = "Please enter valid stock amount"

            elif len(str(stock)) == 0 or stock < 0:
                error = "Please enter valid stock amount"

            elif isinstance(price, float) == False:
                error = "Please enter valid price"

            elif len(str(price)) == 0 or price < 0:
                error = "Please enter valid price"

            else:
                updated = Inventory.query.filter_by(id = id).first()
                updated.name = name
                updated.stock = stock
                updated.price = price
                updated.for_sale = for_sale
                db.session.commit()
                return redirect(url_for("home", username = username))
        
        if delete == True:
            return redirect(url_for("delete", id = id, username = username))

        if back == True:
            return redirect(url_for("home", username = username))

    return render_template('update.html', form = form, message = error, username = username, all = all, id = id)

@app.route('/delete/<username>/<id>', methods = ['GET', 'POST'])
def delete(id, username):
    item = Inventory.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("home", username = username))

@app.route('/admin/edit/<username>', methods = ['GET', 'POST'])
def edit_admin(username):
    error = ""
    form = LoginForm()
    all = Users.query.filter_by(username = username).all()
    
    if request.method == 'POST':
        delete = form.delete.data
        back = form.back.data

        if delete == True:
            return redirect(url_for("admin_delete", username = username))
        
        if back == True:
            return redirect(url_for("admin"))

    return render_template('update_admin.html', form = form, message = error, all = all)

@app.route('/admin/delete/<username>', methods = ['GET', 'POST'])
def admin_delete(username):
    user = Users.query.filter_by(username=username).first()
    user_items = Inventory.query.filter_by(user_id=username).all()
    db.session.delete(user)
    for i in user_items:
        db.session.delete(i)
    db.session.commit()
    return redirect(url_for("admin"))

@app.route('/order/<username>', methods = ['GET', 'POST'])
def order(username):
    error = ""
    form = ItemsForm()
    all = Inventory.query.filter_by(user_id = username).all()

    if request.method == 'POST':
        order = form.order.data
        submit = form.submit.data
        if submit == True:
            if order == "Oldest":
                all = Inventory.query.order_by(Inventory.id).all()
            elif order == "Newest":
                all = Inventory.query.order_by(Inventory.id.desc()).all()
            elif order == "A-Z":
                all = Inventory.query.order_by(Inventory.name).all()
            elif order == "Z-A":
                all = Inventory.query.order_by(Inventory.name.desc()).all()
            elif order == "Stock ↑":
                all = Inventory.query.order_by(Inventory.stock.desc()).all()
            elif order == "Stock ↓":
                all = Inventory.query.order_by(Inventory.stock).all()
            elif order == "Price ↑":
                all = Inventory.query.order_by(Inventory.price.desc()).all()
            elif order == "Price ↓":
                all = Inventory.query.order_by(Inventory.price).all()
            elif order == "For Sale":
                all = Inventory.query.order_by(Inventory.for_sale.desc()).all()
            elif order == "Not For Sale":
                all = Inventory.query.order_by(Inventory.for_sale).all()

    return render_template('home.html', form = form, message = error, username = username, all = all)

# def todo():
#     form = AddForm()
#     all_todo = Todos.query.all()
#     not_complete = Todos.query.filter_by(complete = False).count()
#     length = len(all_todo)

#     return render_template('index.html', form = form, all_todo = all_todo, not_complete = not_complete, length = length)

# @app.route('/add', methods=['GET', 'POST'])
# def add():
#     error = ''
#     form = AddForm()

#     if request.method == 'POST':
#         task = form.task.data
#         submit_task = form.submit_task.data

#         if submit_task == True:
#             if len(task) == 0:
#                 error = "Please enter a task"
#             else:
#                 new_todo = Todos(task=task)
#                 db.session.add(new_todo)
#                 db.session.commit()
#                 return redirect(url_for("todo"))

#     return render_template('add.html', form=form, message=error)

# @app.route('/complete/<id>', methods = ['GET', 'POST'])
# def complete(id):
#     to_do = Todos.query.filter_by(id=id).first()
#     to_do.complete = True
#     db.session.commit()
#     return redirect(url_for("todo"))

# @app.route('/incomplete/<id>', methods = ['GET', 'POST'])
# def incomplete(id):
#     to_do = Todos.query.filter_by(id=id).first()
#     to_do.complete = False
#     db.session.commit()
#     return redirect(url_for("todo"))

# @app.route('/delete/<id>', methods = ['GET', 'POST'])
# def delete(id):
#     to_do = Todos.query.filter_by(id=id).first()
#     db.session.delete(to_do)
#     db.session.commit()
#     return redirect(url_for("todo"))

# @app.route('/update/<id>', methods = ['GET', 'POST'])
# def update(id):

#     error = ''
#     form = AddForm()

#     if request.method == 'POST':
#         task = form.task.data
#         update = form.update.data

#         if update == True:
#             if len(task) == 0:
#                 error = "Please enter a task"
#             else:
#                 to_do = Todos.query.filter_by(id=id).first()
#                 to_do.task = task
#                 db.session.commit()
#                 return redirect(url_for("todo"))

#     return render_template('update.html', form=form, message=error)

# @app.route('/order', methods = ['GET', 'POST'])
# def order():
#     form = AddForm()
#     all_todo = Todos.query.all()
#     not_complete = Todos.query.filter_by(complete = False).count()
#     length = len(all_todo)

#     if request.method == 'POST':
#         order = form.order.data
#         submit = form.submit_order.data
#         if submit == True:
#             if order == "Oldest":
#                 all_todo = Todos.query.order_by(Todos.id).all()
#             elif order == "Newest":
#                 all_todo = Todos.query.order_by(Todos.id.desc()).all()
#             elif order == "Completed":
#                 all_todo = Todos.query.order_by(Todos.complete.desc()).all()
#             elif order == "Not Completed":
#                 all_todo = Todos.query.order_by(Todos.complete).all()

#     return render_template('index.html', form = form, all_todo = all_todo, not_complete = not_complete, length = length)