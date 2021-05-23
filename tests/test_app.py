from flask import url_for
from flask_testing import TestCase

from application import app, db
from application.models import Users, Inventory

class TestBase(TestCase):

    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True,
                WTF_CSRF_ENABLED=False
                )
        return app

    def setUp(self):
        db.create_all()
        sample1 = Users(username = "admin", password = "admin")
        sample2 = Users(username = "andrew", password = "1234")
        db.session.add(sample1)
        db.session.add(sample2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):

    def test_login_username_empty(self):
        response = self.client.post(url_for('login'), data = {"username":"", "login":True}, follow_redirects=True)
        self.assertIn(b"Please enter a valid username", response.data)

    def test_login_password_empty(self):
        response = self.client.post(url_for('login'), data = {"username":"admin", "password":"", "login":True}, follow_redirects=True)
        self.assertIn(b"Please enter a valid password", response.data)

    def test_login_wrong_username(self):
        response = self.client.post(url_for('login'), data = {"username":"wrong", "password":"password", "login":True}, follow_redirects=True)
        self.assertIn(b"Wrong Username", response.data)

    def test_login_wrong_password(self):
        response = self.client.post(url_for('login'), data = {"username":"admin", "password":"wrong", "login":True}, follow_redirects=True)
        self.assertIn(b"Wrong Password", response.data)
    
    def test_login_admin(self):
        response = self.client.post(url_for('login'), data = {"username":"admin", "password":"admin", "login":True}, follow_redirects=True)
        self.assertIn(b"Logged in as: admin", response.data)

    def test_login_user(self):
        response = self.client.post(url_for('login'), data = {"username":"andrew", "password":"1234", "login":True}, follow_redirects=True)
        self.assertIn(b"Logged in as: andrew", response.data)

    def test_login_no_user(self):
        item1 = Users.query.filter_by(username="admin").first()
        item2 = Users.query.filter_by(username="andrew").first()
        db.session.delete(item1)
        db.session.delete(item2)
        db.session.commit()
        response = self.client.post(url_for('login'), data = {"username":"andrew", "password":"1234", "login":True}, follow_redirects=True)
        self.assertIn(b"Wrong Username", response.data)

    def test_create_user(self):
        response = self.client.post(url_for('login'), data = {"register":True}, follow_redirects=True)
        self.assertIn(b"Create a New Account", response.data)

    def test_create_username_empty(self):
        response = self.client.post(url_for('create_user'), data = {"username":"", "password":"1234", "register":True}, follow_redirects=True)
        self.assertIn(b"Please enter a valid username", response.data)

    def test_create_password_empty(self):
        response = self.client.post(url_for('create_user'), data = {"username":"john", "password":"", "register":True}, follow_redirects=True)
        self.assertIn(b"Please enter a valid password", response.data)

    def test_create_empty_database(self):
        item1 = Users.query.filter_by(username="admin").first()
        item2 = Users.query.filter_by(username="andrew").first()
        db.session.delete(item1)
        db.session.delete(item2)
        db.session.commit()
        response = self.client.post(url_for('create_user'), data = {"username":"john", "password":"1234", "register":True}, follow_redirects=True)
        self.assertIn(b"Login", response.data)

    def test_create_user_exists(self):
        response = self.client.post(url_for('create_user'), data = {"username":"andrew", "password":"abc", "register":True}, follow_redirects=True)
        self.assertIn(b"Username already exists.", response.data)

    def test_create_new_user(self):
        response = self.client.post(url_for('create_user'), data = {"username":"john", "password":"abc", "register":True}, follow_redirects=True)
        self.assertIn(b"Login", response.data)

    def test_add_empty_name(self):
        response = self.client.post(url_for('add', username = "andrew"), data = {"name":"", "stock":1, "price":10, "for_sale":True, "add_item":True}, follow_redirects=True)
        self.assertIn(b"Please enter an item name", response.data)

    def test_add_invalid_stock_not_integer(self):
        response = self.client.post(url_for('add', username = "andrew"), data = {"name":"test", "stock":"wrong", "price":10, "for_sale":True, "add_item":True}, follow_redirects=True)
        self.assertIn(b"Please enter valid stock amount", response.data)

    def test_add_invalid_stock_negative(self):
        response = self.client.post(url_for('add', username = "andrew"), data = {"name":"test", "stock":-1, "price":10, "for_sale":True, "add_item":True}, follow_redirects=True)
        self.assertIn(b"Please enter valid stock amount", response.data)

    def test_add_invalid_price_not_float(self):
        response = self.client.post(url_for('add', username = "andrew"), data = {"name":"test", "stock":1, "price":"wrong", "for_sale":True, "add_item":True}, follow_redirects=True)
        self.assertIn(b"Please enter valid price", response.data)

    def test_add_invalid_price_negative(self):
        response = self.client.post(url_for('add', username = "andrew"), data = {"name":"test", "stock":1, "price":-1, "for_sale":True, "add_item":True}, follow_redirects=True)
        self.assertIn(b"Please enter valid price", response.data)

    def test_add_item(self):
        response = self.client.post(url_for('add', username = "andrew"), data = {"name":"test", "stock":1, "price":1, "for_sale":True, "add_item":True}, follow_redirects=True)
        self.assertIn(b"Logged in as: andrew", response.data)

    def test_back_add(self):
        response = self.client.post(url_for('add', username = "andrew"), data = {"back":True}, follow_redirects=True)
        self.assertIn(b"Logged in as: andrew", response.data)

    def test_update_empty_name(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        response = self.client.post(url_for('update', username = "andrew", id = sample_item.id), data = {"name":"", "update":True}, follow_redirects=True)
        self.assertIn(b"Please enter an item name", response.data)

    def test_update_page(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        response = self.client.get(url_for('update', username = "andrew", id = sample_item.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'jacket', response.data)

    def test_update_stock_not_integer(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        response = self.client.post(url_for('update', username = "andrew", id = sample_item.id), data = {"name":"jacket", "stock":"wrong", "price":50, "for_sale":True, "update":True}, follow_redirects=True)
        self.assertIn(b"Please enter valid stock amount", response.data)

    def test_update_stock_negative(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        response = self.client.post(url_for('update', username = "andrew", id = sample_item.id), data = {"name":"jacket", "stock":-1, "price":50, "for_sale":True, "update":True}, follow_redirects=True)
        self.assertIn(b"Please enter valid stock amount", response.data)

    def test_update_price_not_float(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        response = self.client.post(url_for('update', username = "andrew", id = sample_item.id), data = {"name":"jacket", "stock":1, "price":"wrong", "for_sale":True, "update":True}, follow_redirects=True)
        self.assertIn(b"Please enter valid price", response.data)

    def test_update_price_negative(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        response = self.client.post(url_for('update', username = "andrew", id = sample_item.id), data = {"name":"jacket", "stock":1, "price":-1, "for_sale":True, "update":True}, follow_redirects=True)
        self.assertIn(b"Please enter valid price", response.data)

    def test_update_successful(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        response = self.client.post(url_for('update', username = "andrew", id = sample_item.id), data = {"name":"shirt", "stock":1, "price":1, "for_sale":True, "update":True}, follow_redirects=True)
        self.assertIn(b"shirt", response.data)

    def test_delete(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        response = self.client.post(url_for('update', username = "andrew", id = sample_item.id), data = {"delete":True}, follow_redirects=True)
        self.assertIn(b"Logged in as: andrew", response.data)

    def test_back_update(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        response = self.client.post(url_for('update', username = "andrew", id = sample_item.id), data = {"back":True}, follow_redirects=True)
        self.assertIn(b"Logged in as: andrew", response.data)

    def test_admin_delete_user(self):
        response = self.client.post(url_for('edit_admin', username = "andrew"), data = {"delete":True}, follow_redirects=True)
        self.assertIn(b'<a href = /admin/edit/admin>Edit Details</a>', response.data)

    def test_back_admin(self):
        response = self.client.post(url_for('edit_admin', username = "andrew"), data = {"back":True}, follow_redirects=True)
        self.assertIn(b'<a href = /admin/edit/andrew>Edit Details</a>', response.data)

    def test_update_admin_page(self):
        response = self.client.get(url_for('edit_admin', username = "andrew"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<label for="username">Username</label>: andrew', response.data)

    def test_delete_user_page(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        response = self.client.get(url_for('admin_delete', username = "andrew"))
        self.assertEqual(response.status_code, 302)
        self.assertNotIsInstance("andrew", Users)
        self.assertNotIsInstance("andrew", Inventory)

    def test_order_oldest(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        sample_item2 = Inventory(name = "strawberry", stock = 4, price = 1, for_sale = False, user_id = "andrew")
        sample_item3 = Inventory(name = "blueberry", stock = 20, price = 5, for_sale = False, user_id = "andrew")
        db.session.add(sample_item)
        db.session.add(sample_item2)
        db.session.add(sample_item3)
        db.session.commit()
        self.client.post(url_for('order', username = "andrew"), data = {"submit":True, "order":"Oldest"}, follow_redirects=True)
        oldest = Inventory.query.order_by(Inventory.id).first()
        self.assertEqual(oldest.id, sample_item.id)

    def test_order_newest(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        sample_item2 = Inventory(name = "strawberry", stock = 4, price = 1, for_sale = False, user_id = "andrew")
        sample_item3 = Inventory(name = "blueberry", stock = 20, price = 5, for_sale = False, user_id = "andrew")
        db.session.add(sample_item)
        db.session.add(sample_item2)
        db.session.add(sample_item3)
        db.session.commit()
        self.client.post(url_for('order', username = "andrew"), data = {"submit":True, "order":"Newest"}, follow_redirects=True)
        newest = Inventory.query.order_by(Inventory.id.desc()).first()
        self.assertEqual(newest.id, sample_item3.id)

    def test_order_a_to_z(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        sample_item2 = Inventory(name = "strawberry", stock = 4, price = 1, for_sale = False, user_id = "andrew")
        sample_item3 = Inventory(name = "blueberry", stock = 20, price = 5, for_sale = False, user_id = "andrew")
        db.session.add(sample_item)
        db.session.add(sample_item2)
        db.session.add(sample_item3)
        db.session.commit()
        self.client.post(url_for('order', username = "andrew"), data = {"submit":True, "order":"A-Z"}, follow_redirects=True)
        a_to_z = Inventory.query.order_by(Inventory.name).first()
        self.assertEqual(a_to_z.name, sample_item3.name)

    def test_order_z_to_a(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        sample_item2 = Inventory(name = "strawberry", stock = 4, price = 1, for_sale = False, user_id = "andrew")
        sample_item3 = Inventory(name = "blueberry", stock = 20, price = 5, for_sale = False, user_id = "andrew")
        db.session.add(sample_item)
        db.session.add(sample_item2)
        db.session.add(sample_item3)
        db.session.commit()
        self.client.post(url_for('order', username = "andrew"), data = {"submit":True, "order":"Z-A"}, follow_redirects=True)
        z_to_a = Inventory.query.order_by(Inventory.name.desc()).first()
        self.assertEqual(z_to_a.name, sample_item2.name)

    def test_order_stock_big_to_small(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        sample_item2 = Inventory(name = "strawberry", stock = 4, price = 1, for_sale = False, user_id = "andrew")
        sample_item3 = Inventory(name = "blueberry", stock = 20, price = 5, for_sale = False, user_id = "andrew")
        db.session.add(sample_item)
        db.session.add(sample_item2)
        db.session.add(sample_item3)
        db.session.commit()
        self.client.post(url_for('order', username = "andrew"), data = {"submit":True, "order":"Stock ↑"}, follow_redirects=True)
        big_to_small = Inventory.query.order_by(Inventory.stock.desc()).first()
        self.assertEqual(big_to_small.stock, sample_item3.stock)

    def test_order_stock_small_to_big(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        sample_item2 = Inventory(name = "strawberry", stock = 4, price = 1, for_sale = False, user_id = "andrew")
        sample_item3 = Inventory(name = "blueberry", stock = 20, price = 5, for_sale = False, user_id = "andrew")
        db.session.add(sample_item)
        db.session.add(sample_item2)
        db.session.add(sample_item3)
        db.session.commit()
        self.client.post(url_for('order', username = "andrew"), data = {"submit":True, "order":"Stock ↓"}, follow_redirects=True)
        small_to_big = Inventory.query.order_by(Inventory.stock).first()
        self.assertEqual(small_to_big.stock, sample_item.stock)

    def test_order_price_big_to_small(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        sample_item2 = Inventory(name = "strawberry", stock = 4, price = 1, for_sale = False, user_id = "andrew")
        sample_item3 = Inventory(name = "blueberry", stock = 20, price = 5, for_sale = False, user_id = "andrew")
        db.session.add(sample_item)
        db.session.add(sample_item2)
        db.session.add(sample_item3)
        db.session.commit()
        self.client.post(url_for('order', username = "andrew"), data = {"submit":True, "order":"Price ↑"}, follow_redirects=True)
        big_to_small = Inventory.query.order_by(Inventory.price.desc()).first()
        self.assertEqual(big_to_small.price, sample_item.price)

    def test_order_price_small_to_big(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        sample_item2 = Inventory(name = "strawberry", stock = 4, price = 1, for_sale = False, user_id = "andrew")
        sample_item3 = Inventory(name = "blueberry", stock = 20, price = 5, for_sale = False, user_id = "andrew")
        db.session.add(sample_item)
        db.session.add(sample_item2)
        db.session.add(sample_item3)
        db.session.commit()
        self.client.post(url_for('order', username = "andrew"), data = {"submit":True, "order":"Price ↓"}, follow_redirects=True)
        small_to_big = Inventory.query.order_by(Inventory.price).first()
        self.assertEqual(small_to_big.price, sample_item2.price)

    def test_order_for_sale(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        sample_item2 = Inventory(name = "strawberry", stock = 4, price = 1, for_sale = False, user_id = "andrew")
        sample_item3 = Inventory(name = "blueberry", stock = 20, price = 5, for_sale = False, user_id = "andrew")
        db.session.add(sample_item)
        db.session.add(sample_item2)
        db.session.add(sample_item3)
        db.session.commit()
        self.client.post(url_for('order', username = "andrew"), data = {"submit":True, "order":"For Sale"}, follow_redirects=True)
        for_sale = Inventory.query.order_by(Inventory.for_sale.desc()).first()
        self.assertEqual(for_sale.for_sale, sample_item.for_sale)

    def test_order_not_for_sale(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        sample_item2 = Inventory(name = "strawberry", stock = 4, price = 1, for_sale = False, user_id = "andrew")
        sample_item3 = Inventory(name = "blueberry", stock = 20, price = 5, for_sale = False, user_id = "andrew")
        db.session.add(sample_item)
        db.session.add(sample_item2)
        db.session.add(sample_item3)
        db.session.commit()
        self.client.post(url_for('order', username = "andrew"), data = {"submit":True, "order":"Not For Sale"}, follow_redirects=True)
        not_for_sale = Inventory.query.order_by(Inventory.for_sale).first()
        self.assertEqual(not_for_sale.for_sale, sample_item2.for_sale)

    def test_back_buy(self):
        response = self.client.post(url_for('buy', username = "andrew"), data = {"back":True}, follow_redirects=True)
        self.assertIn(b"Logged in as: andrew", response.data)

    def test_buy(self):
        sample1 = Users(username = "billy", password = "234")
        db.session.add(sample1)
        sample_item = Inventory(name = "chicken", stock = 2, price = 10, for_sale = True, user_id = "billy")
        db.session.add(sample_item)
        db.session.commit()
        response = self.client.get(url_for('buy', username = "andrew"))
        self.assertIn(b"chicken", response.data)

    def test_checkout(self):
        sample1 = Users(username = "billy", password = "234")
        db.session.add(sample1)
        sample_item = Inventory(name = "chicken", stock = 2, price = 10, for_sale = True, user_id = "billy")
        db.session.add(sample_item)
        db.session.commit()
        self.client.get(url_for('cart', username = "andrew", id = sample_item.id))
        self.assertEqual(sample_item.stock, 1)

    def test_checkout_no_stock(self):
        sample1 = Users(username = "billy", password = "234")
        db.session.add(sample1)
        sample_item = Inventory(name = "chicken", stock = 1, price = 10, for_sale = True, user_id = "billy")
        db.session.add(sample_item)
        db.session.commit()
        self.client.get(url_for('cart', username = "andrew", id = sample_item.id))
        self.assertEqual(sample_item.for_sale, False)