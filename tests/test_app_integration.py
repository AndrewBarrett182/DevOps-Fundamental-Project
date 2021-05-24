from selenium import webdriver
from flask_testing import LiveServerTestCase
from urllib.request import urlopen
from flask import url_for

from application import app, db
from application.models import Users, Inventory


class TestBase(LiveServerTestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
        app.config['SECRET_KEY'] = "1234567890"
        app.config['LIVESERVER_PORT'] = 5000
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        return app

    def setUp(self):
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=chrome_options) 

        db.create_all()
        sample1 = Users(username = "admin", password = "admin")
        sample2 = Users(username = "andrew", password = "1234")
        db.session.add(sample1)
        db.session.add(sample2)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/')

    def tearDown(self):
        self.driver.quit()
        db.drop_all()

    def test_server_running(self):
        response = urlopen("http://localhost:5000/")
        self.assertEqual(response.code, 200)

class TestCreate(TestBase):

    def test_login_username_empty(self):
        self.driver.get(f'http://localhost:5000/')
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('')
        self.driver.find_element_by_xpath('//*[@id="login"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter a valid username", text)

    def test_login_password_empty(self):
        self.driver.get(f'http://localhost:5000/')
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('admin')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys('')
        self.driver.find_element_by_xpath('//*[@id="login"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter a valid password", text)

    def test_login_wrong_username(self):
        self.driver.get(f'http://localhost:5000/')
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('wrong')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys('password')
        self.driver.find_element_by_xpath('//*[@id="login"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Wrong Username", text)
        
    def test_login_wrong_password(self):
        self.driver.get(f'http://localhost:5000/')
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('admin')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys('wrong')
        self.driver.find_element_by_xpath('//*[@id="login"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Wrong Password", text)

    def test_login_admin(self):
        self.driver.get(f'http://localhost:5000/')
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('admin')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys('admin')
        self.driver.find_element_by_xpath('//*[@id="login"]').click()
        self.assertIn(url_for('admin'), self.driver.current_url)

    def test_login_user(self):
        self.driver.get(f'http://localhost:5000/')
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('andrew')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys('1234')
        self.driver.find_element_by_xpath('//*[@id="login"]').click()
        self.assertIn(url_for('home', username = "andrew"), self.driver.current_url)

    def test_login_no_user(self):
        item1 = Users.query.filter_by(username="admin").first()
        item2 = Users.query.filter_by(username="andrew").first()
        db.session.delete(item1)
        db.session.delete(item2)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/')
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('andrew')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys('1234')
        self.driver.find_element_by_xpath('//*[@id="login"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Wrong Username", text)

    def test_create_user(self):
        self.driver.get(f'http://localhost:5000/')
        self.driver.find_element_by_xpath('//*[@id="register"]').click()
        self.assertIn(url_for('create_user'), self.driver.current_url)

    def test_create_username_empty(self):
        self.driver.get(f'http://localhost:5000/register')
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys('1234')
        self.driver.find_element_by_xpath('//*[@id="register"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter a valid username", text)

    def test_create_password_empty(self):
        self.driver.get(f'http://localhost:5000/register')
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('john')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys('')
        self.driver.find_element_by_xpath('//*[@id="register"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter a valid password", text)
    
    def test_create_empty_database(self):
        item1 = Users.query.filter_by(username="admin").first()
        item2 = Users.query.filter_by(username="andrew").first()
        db.session.delete(item1)
        db.session.delete(item2)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/register')
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('john')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys('1234')
        self.driver.find_element_by_xpath('//*[@id="register"]').click()
        self.assertIn(url_for('login'), self.driver.current_url)

    def test_create_user_exists(self):
        self.driver.get(f'http://localhost:5000/register')
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('andrew')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys('abc')
        self.driver.find_element_by_xpath('//*[@id="register"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Username already exists.", text)

    def test_create_new_user(self):
        self.driver.get(f'http://localhost:5000/register')
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('john')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys('abc')
        self.driver.find_element_by_xpath('//*[@id="register"]').click()
        self.assertIn(url_for('login'), self.driver.current_url)

    def test_add_empty_name(self):
        self.driver.get(f'http://localhost:5000/add/andrew')
        name = self.driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys('')
        stock = self.driver.find_element_by_xpath('//*[@id="stock"]')
        stock.send_keys('1')
        price = self.driver.find_element_by_xpath('//*[@id="price"]')
        price.send_keys('10')
        self.driver.find_element_by_xpath('//*[@id="for_sale"]').click()
        self.driver.find_element_by_xpath('//*[@id="add_item"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter an item name", text)
    
    def test_add_invalid_stock_not_integer(self):
        self.driver.get(f'http://localhost:5000/add/andrew')
        name = self.driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys('test')
        stock = self.driver.find_element_by_xpath('//*[@id="stock"]')
        stock.send_keys('wrong')
        price = self.driver.find_element_by_xpath('//*[@id="price"]')
        price.send_keys('10')
        self.driver.find_element_by_xpath('//*[@id="for_sale"]').click()
        self.driver.find_element_by_xpath('//*[@id="add_item"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter valid stock amount", text)

    def test_add_invalid_stock_negative(self):
        self.driver.get(f'http://localhost:5000/add/andrew')
        name = self.driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys('test')
        stock = self.driver.find_element_by_xpath('//*[@id="stock"]')
        stock.send_keys('-1')
        price = self.driver.find_element_by_xpath('//*[@id="price"]')
        price.send_keys('10')
        self.driver.find_element_by_xpath('//*[@id="for_sale"]').click()
        self.driver.find_element_by_xpath('//*[@id="add_item"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter valid stock amount", text)

    def test_add_invalid_price_not_float(self):
        self.driver.get(f'http://localhost:5000/add/andrew')
        name = self.driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys('test')
        stock = self.driver.find_element_by_xpath('//*[@id="stock"]')
        stock.send_keys('1')
        price = self.driver.find_element_by_xpath('//*[@id="price"]')
        price.send_keys('wrong')
        self.driver.find_element_by_xpath('//*[@id="for_sale"]').click()
        self.driver.find_element_by_xpath('//*[@id="add_item"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter valid price", text)

    def test_add_invalid_price_negative(self):
        self.driver.get(f'http://localhost:5000/add/andrew')
        name = self.driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys('test')
        stock = self.driver.find_element_by_xpath('//*[@id="stock"]')
        stock.send_keys('1')
        price = self.driver.find_element_by_xpath('//*[@id="price"]')
        price.send_keys('-1')
        self.driver.find_element_by_xpath('//*[@id="for_sale"]').click()
        self.driver.find_element_by_xpath('//*[@id="add_item"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter valid price", text)

    def test_add_item(self):
        self.driver.get(f'http://localhost:5000/add/andrew')
        name = self.driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys('test')
        stock = self.driver.find_element_by_xpath('//*[@id="stock"]')
        stock.send_keys('1')
        price = self.driver.find_element_by_xpath('//*[@id="price"]')
        price.send_keys('1')
        self.driver.find_element_by_xpath('//*[@id="for_sale"]').click()
        self.driver.find_element_by_xpath('//*[@id="add_item"]').click()
        self.assertIn(url_for('home', username = "andrew"), self.driver.current_url)

    def test_back_add(self):
        self.driver.get(f'http://localhost:5000/add/andrew')
        self.driver.find_element_by_xpath('//*[@id="back"]').click()
        self.assertIn(url_for('home', username = "andrew"), self.driver.current_url)

    def test_update_empty_name(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/home/andrew')
        self.driver.find_element_by_xpath('/html/body/div[2]/a').click()
        name = self.driver.find_element_by_xpath('//*[@id="name"]')
        name.clear()
        name.send_keys('')
        self.driver.find_element_by_xpath('//*[@id="update"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter an item name", text)

    def test_update_page(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/home/andrew')
        self.driver.find_element_by_xpath('/html/body/div[2]/a').click()
        self.assertIn(url_for('update', username = "andrew", id = sample_item.id), self.driver.current_url)

    def test_update_stock_not_integer(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/update/andrew/{sample_item.id}')
        stock = self.driver.find_element_by_xpath('//*[@id="stock"]')
        stock.send_keys('wrong')
        self.driver.find_element_by_xpath('//*[@id="update"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter valid stock amount", text)

    def test_update_stock_negative(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/update/andrew/{sample_item.id}')
        stock = self.driver.find_element_by_xpath('//*[@id="stock"]')
        stock.send_keys('-1')
        self.driver.find_element_by_xpath('//*[@id="update"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter valid stock amount", text)

    def test_update_price_not_float(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/update/andrew/{sample_item.id}')
        price = self.driver.find_element_by_xpath('//*[@id="price"]')
        price.send_keys('wrong')
        self.driver.find_element_by_xpath('//*[@id="update"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter valid price", text)

    def test_update_price_negative(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/update/andrew/{sample_item.id}')
        price = self.driver.find_element_by_xpath('//*[@id="price"]')
        price.send_keys('-1')
        self.driver.find_element_by_xpath('//*[@id="update"]').click()
        text = self.driver.find_element_by_xpath('/html/body/div[1]/form').text
        self.assertIn("Please enter valid price", text)

    def test_update_successful(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/update/andrew/{sample_item.id}')
        name = self.driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys('shirt')
        self.driver.find_element_by_xpath('//*[@id="update"]').click()
        self.assertIn(url_for('home', username = "andrew"), self.driver.current_url)

    def test_delete(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/update/andrew/{sample_item.id}')
        self.driver.find_element_by_xpath('//*[@id="delete"]').click()
        self.assertIn(url_for('home', username = "andrew"), self.driver.current_url)

    def test_back_update(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/update/andrew/{sample_item.id}')
        self.driver.find_element_by_xpath('//*[@id="back"]').click()
        self.assertIn(url_for('home', username = "andrew"), self.driver.current_url)

    def test_admin_delete_user(self):
        self.driver.get(f'http://localhost:5000/admin/edit/andrew')
        self.driver.find_element_by_xpath('//*[@id="delete"]').click()
        self.assertIn(url_for('admin'), self.driver.current_url)

    def test_back_admin(self):
        self.driver.get(f'http://localhost:5000/admin/edit/andrew')
        self.driver.find_element_by_xpath('//*[@id="back"]').click()
        self.assertIn(url_for('admin'), self.driver.current_url)

    def test_update_admin_page(self):
        self.driver.get(f'http://localhost:5000/admin/edit/andrew')
        text = self.driver.find_element_by_xpath('/html/body/div[2]/form').text
        self.assertIn('Username: andrew', text)

    def test_delete_user_page(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/admin/delete/andrew')
        self.assertIn(url_for('admin'), self.driver.current_url)

    def test_order_oldest(self):
        sample_item = Inventory(name = "jacket", stock = 1, price = 50, for_sale = True, user_id = "andrew")
        sample_item2 = Inventory(name = "strawberry", stock = 4, price = 1, for_sale = False, user_id = "andrew")
        sample_item3 = Inventory(name = "blueberry", stock = 20, price = 5, for_sale = False, user_id = "andrew")
        db.session.add(sample_item)
        db.session.add(sample_item2)
        db.session.add(sample_item3)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/home/andrew')
        self.driver.find_element_by_xpath('//*[@id="order"]').click()
        self.driver.find_element_by_xpath('//*[@id="order"]/option[1]').click()
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
        self.driver.get(f'http://localhost:5000/home/andrew')
        self.driver.find_element_by_xpath('//*[@id="order"]').click()
        self.driver.find_element_by_xpath('//*[@id="order"]/option[2]').click()
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
        self.driver.get(f'http://localhost:5000/home/andrew')
        self.driver.find_element_by_xpath('//*[@id="order"]').click()
        self.driver.find_element_by_xpath('//*[@id="order"]/option[3]').click()
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
        self.driver.get(f'http://localhost:5000/home/andrew')
        self.driver.find_element_by_xpath('//*[@id="order"]').click()
        self.driver.find_element_by_xpath('//*[@id="order"]/option[4]').click()
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
        self.driver.get(f'http://localhost:5000/home/andrew')
        self.driver.find_element_by_xpath('//*[@id="order"]').click()
        self.driver.find_element_by_xpath('//*[@id="order"]/option[5]').click()
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
        self.driver.get(f'http://localhost:5000/home/andrew')
        self.driver.find_element_by_xpath('//*[@id="order"]').click()
        self.driver.find_element_by_xpath('//*[@id="order"]/option[6]').click()
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
        self.driver.get(f'http://localhost:5000/home/andrew')
        self.driver.find_element_by_xpath('//*[@id="order"]').click()
        self.driver.find_element_by_xpath('//*[@id="order"]/option[7]').click()
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
        self.driver.get(f'http://localhost:5000/home/andrew')
        self.driver.find_element_by_xpath('//*[@id="order"]').click()
        self.driver.find_element_by_xpath('//*[@id="order"]/option[8]').click()
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
        self.driver.get(f'http://localhost:5000/home/andrew')
        self.driver.find_element_by_xpath('//*[@id="order"]').click()
        self.driver.find_element_by_xpath('//*[@id="order"]/option[9]').click()
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
        self.driver.get(f'http://localhost:5000/home/andrew')
        self.driver.find_element_by_xpath('//*[@id="order"]').click()
        self.driver.find_element_by_xpath('//*[@id="order"]/option[10]').click()
        not_for_sale = Inventory.query.order_by(Inventory.for_sale).first()
        self.assertEqual(not_for_sale.for_sale, sample_item2.for_sale)

    def test_back_buy(self):
        self.driver.get(f'http://localhost:5000/buy/andrew')
        self.driver.find_element_by_xpath('//*[@id="back"]').click()
        self.assertIn(url_for('home', username = "andrew"), self.driver.current_url)

    def test_buy(self):
        sample1 = Users(username = "billy", password = "234")
        db.session.add(sample1)
        sample_item = Inventory(name = "chicken", stock = 2, price = 10, for_sale = True, user_id = "billy")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/buy/andrew')
        text = self.driver.find_element_by_xpath('/html/body').text
        self.assertIn('chicken', text)

    def test_checkout(self):
        sample1 = Users(username = "billy", password = "234")
        db.session.add(sample1)
        sample_item = Inventory(name = "chicken", stock = 2, price = 10, for_sale = True, user_id = "billy")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/cart/andrew/{sample_item.id}')
        text = self.driver.find_element_by_xpath('/html/body').text
        self.assertIn("Stock: 1", text)

    def test_checkout_no_stock(self):
        sample1 = Users(username = "billy", password = "234")
        db.session.add(sample1)
        sample_item = Inventory(name = "chicken", stock = 1, price = 10, for_sale = True, user_id = "billy")
        db.session.add(sample_item)
        db.session.commit()
        self.driver.get(f'http://localhost:5000/cart/andrew/{sample_item.id}')
        text = self.driver.find_element_by_xpath('/html/body').text
        self.assertIn(url_for('buy', username = "andrew"), self.driver.current_url)
    
