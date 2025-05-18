import sys
import os
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
                            QLabel, QComboBox, QListWidget, QWidget, QMessageBox)
from datetime import datetime
import hashlib # Şifre hashleme için eklendi

# Yardımcı fonksiyonlar için ayrı bir dosya (utils.py) oluşturabilirsiniz
def read_json_file(filename, default_value=[]):
    """JSON dosyasını okur, hata durumunda belirtilen varsayılan değeri döndürür."""
    if not os.path.exists(filename):
        return default_value
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        QMessageBox.critical(None, "Hata", f"{filename} dosyası okunurken bir hata oluştu.")
        return default_value
    except Exception as e:
        QMessageBox.critical(None, "Hata", f"{filename} dosyası okunurken bir hata oluştu: {e}")
        return default_value

def write_json_file(filename, data):
    """Veriyi JSON dosyasına yazar, hata durumunda kullanıcıya bildirir."""
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        QMessageBox.critical(None, "Hata", f"{filename} dosyasına yazılırken bir hata oluştu: {e}")

def hash_password(password):
    """Şifreyi hashler."""
    return hashlib.sha256(password.encode()).hexdigest()

# Stil tanımlarını içeren bir dosya (style.qss) oluşturun
style_sheet = """
QMainWindow {
    background-color: #f5f5dc; /* Krem */
    font-family: "Segoe UI", sans-serif;
}

/* Giriş Penceresi Stilleri */
QMainWindow#loginWindow {
    background-color: #fff8e1; /* Açık Krem */
}

QLineEdit {
    padding: 10px;
    border: 1px solid #d7ccc8; /* Açık Kahverengi */
    border-radius: 5px;
    font-size: 16px;
    background-color: white;
    color: #4e342e; /* Koyu Kahverengi */
}

QPushButton {
    background-color: #a1887f; /* Orta Kahverengi */
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 7px;
    font-size: 18px;
    cursor: pointer;
}

QPushButton:hover {
    background-color: #795548; /* Daha Koyu Kahverengi */
}

QLabel {
    font-size: 16px;
    margin-bottom: 5px;
    color: #4e342e; /* Koyu Kahverengi */
}

/* Kayıt Penceresi Stilleri */
QMainWindow#registerWindow {
    background-color: #fbe9e7; /* Daha Açık Kahverengi */
}

/* Ana Pencere Stilleri */
QMainWindow#mainWindow {
    background-color: #e0f2f1; /* Açık Yeşilimsi Krem */
}

QMainWindow#mainWindow QPushButton {
    background-color: #5d4037; /* Koyu Kahverengi */
}

QMainWindow#mainWindow QPushButton:hover {
    background-color: #4e342e; /* Daha Koyu Kahverengi */
}

/* Sipariş Verme Penceresi Stilleri */
QMainWindow#orderWindow {
    background-color: #fff3e0; /* Açık Turuncumsu Krem */
}

QComboBox {
    padding: 10px;
    border: 1px solid #d7ccc8; /* Açık Kahverengi */
    border-radius: 5px;
    font-size: 16px;
    background-color: white;
    color: #4e342e; /* Koyu Kahverengi */
}

QListWidget {
    border: 1px solid #d7ccc8; /* Açık Kahverengi */
    border-radius: 5px;
    font-size: 14px;
    padding: 8px;
    background-color: white;
    color: #4e342e; /* Koyu Kahverengi */
}

/* Siparişlerim Penceresi Stilleri */
QMainWindow#myOrdersWindow {
    background-color: #e8f5e9; /* Açık Yeşilimsi Krem */
}

/* Hesap Bilgileri Penceresi Stilleri */
QMainWindow#accountWindow {
    background-color: #ffebee; /* Açık Pembeimsi Krem */
}

/* Yeni Adres Ekleme Penceresi Stilleri */
QMainWindow#addAddressWindow {
    background-color: #f3e5f5; /* Açık Lavanta Krem */
}

/* Hesap Bilgilerini Düzenleme Penceresi Stilleri */
QMainWindow#editAccountWindow {
    background-color: #ede7f6; /* Daha Açık Lavanta Krem */
}
"""

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Yap")
        self.setGeometry(100, 100, 400, 200)
        self.setObjectName("loginWindow")

        layout = QFormLayout()

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Telefon")
        layout.addRow("Telefon:", self.phone_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Şifre")
        layout.addRow("Şifre:", self.password_input)

        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Kayıt Ol")
        self.register_button.clicked.connect(self.open_register)
        layout.addWidget(self.register_button)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    def login(self):
        phone = self.phone_input.text()
        password = self.password_input.text()
        users = read_json_file("users.json")
        for user in users:
            # Şifreyi hashleyerek karşılaştırın
            if user["phone"] == phone and user["password"] == hash_password(password):
                self.main_window = MainWindow(user["name"], user["phone"], user["password"])
                self.main_window.show()
                self.close()
                return
        QMessageBox.warning(self, "Hata", "Telefon veya şifre yanlış!")

    def open_register(self):
        self.register_window = RegistrationWindow()
        self.register_window.show()
        self.close()

class RegistrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kayıt Ol")
        self.setGeometry(100, 100, 400, 300)
        self.setObjectName("registerWindow")

        layout = QFormLayout()

        self.name_input = QLineEdit()
        layout.addRow("Ad Soyad:", self.name_input)

        self.phone_input = QLineEdit()
        layout.addRow("Telefon:", self.phone_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("Şifre:", self.password_input)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Adres")
        layout.addRow("Adres:", self.address_input)

        self.register_button = QPushButton("Kayıt Ol")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    def register(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        password = self.password_input.text()
        address = self.address_input.text()

        if not name or not phone or not password or not address:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
            return

        users = read_json_file("users.json", []) # Dosya yoksa boş liste ile başla
        for user in users:
            if user["phone"] == phone:
                QMessageBox.warning(self, "Hata", "Bu telefon numarasıyla zaten kayıt olunmuş.")
                return

        # Şifreyi hashleyerek sakla
        hashed_password = hash_password(password)
        user_data = {"name": name, "phone": phone, "password": hashed_password, "addresses": [address]}
        users.append(user_data)
        write_json_file("users.json", users)

        QMessageBox.information(self, "Başarılı", "Kayıt başarılı. Giriş yapabilirsiniz.")
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

class MainWindow(QMainWindow):
    def __init__(self, name, phone, password):
        super().__init__()
        self.setWindowTitle("Ana Ekran")
        self.setGeometry(100, 100, 400, 300)
        self.setObjectName("mainWindow")

        self.name = name
        self.phone = phone
        self.password = password

        layout = QVBoxLayout()

        self.order_button = QPushButton("Sipariş Ver")
        self.order_button.clicked.connect(self.open_order_window)
        layout.addWidget(self.order_button)

        self.my_orders_button = QPushButton("Siparişlerim")
        self.my_orders_button.clicked.connect(self.open_my_orders_window)
        layout.addWidget(self.my_orders_button)

        self.account_button = QPushButton("Hesap Bilgileri")
        self.account_button.clicked.connect(self.open_account_window)
        layout.addWidget(self.account_button)

        self.exit_button = QPushButton("Çıkış")
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_order_window(self):
        self.order_window = OrderWindow(self.phone)
        self.order_window.show()

    def open_my_orders_window(self):
        self.my_orders_window = MyOrdersWindow(self.phone)
        self.my_orders_window.show()

    def open_account_window(self):
        self.account_window = AccountWindow(self.name, self.phone, self.password)
        self.account_window.show()

class OrderWindow(QMainWindow):
    def __init__(self, user_phone):
        super().__init__()
        self.setWindowTitle("Sipariş Verme Ekranı")
        self.setGeometry(100, 100, 400, 400)
        self.setObjectName("orderWindow")
        self.user_phone = user_phone
        self.user_addresses = self.load_user_addresses()

        layout = QVBoxLayout()

        self.address_combo = QComboBox()
        self.address_combo.addItem("Adres Seçin")
        self.address_combo.addItems(self.user_addresses)
        layout.addWidget(self.address_combo)

        self.food_data = {
            "Tatlılar": {
                "Tiramisu": 28,
                "Sütlaç": 22
            },
            "Ev Yemekleri": {
                "Tavuk Sote": 35,
                "Mercimek Çorbası": 25,
                "Mantı": 65,
                "Köfte": 40
            },
            "Deniz Ürünleri": {
                "Izgara Somon": 75,
                "Suşi": 60
            },
            "Fast Food": {
                "Pizza": 50,
                "Burger": 30,
                "Pide": 45,
                "Kebap": 55,
                "Noodle": 38
            },
            "Salatalar": {
                "Salata": 20
            },
            "Pastane": {
                "Pasta": 40
            },
            "İçecekler": {
                "Su": 5,
                "Ayran": 8,
                "Kola": 10
            }
        }

        self.category_combo = QComboBox()
        self.category_combo.addItem("Kategori Seçin")
        self.category_combo.addItems(self.food_data.keys())
        self.category_combo.currentIndexChanged.connect(self.update_food_list)
        layout.addWidget(self.category_combo)

        self.food_list = QComboBox()
        self.food_list.addItem("Yemek Seçin")
        layout.addWidget(self.food_list)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Miktar")
        layout.addWidget(self.quantity_input)

        self.add_to_cart_button = QPushButton("Sepete Ekle")
        self.add_to_cart_button.clicked.connect(self.add_to_cart)
        layout.addWidget(self.add_to_cart_button)

        self.cart_list = QListWidget()
        layout.addWidget(self.cart_list)

        self.total_label = QLabel("Toplam Tutar: 0 TL")
        layout.addWidget(self.total_label)

        self.submit_order_button = QPushButton("Siparişi Ver")
        self.submit_order_button.clicked.connect(self.submit_order)
        layout.addWidget(self.submit_order_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.total_price = 0
        self.cart_items = []

    def load_user_addresses(self):
        """Kullanıcının kayıtlı adreslerini users.json dosyasından yükler."""
        users = read_json_file("users.json")
        for user in users:
            if user["phone"] == self.user_phone:
                return user.get("addresses", [])
        return []

    def update_food_list(self, index):
        self.food_list.clear()
        self.food_list.addItem("Yemek Seçin")
        selected_category = self.category_combo.itemText(index)
        if selected_category in self.food_data:
            self.food_list.addItems(self.food_data[selected_category].keys())

    def add_to_cart(self):
        selected_food = self.food_list.currentText()
        quantity_text = self.quantity_input.text()

        if selected_food == "Yemek Seçin":
            QMessageBox.warning(self, "Uyarı", "Lütfen bir yemek seçin.")
            return

        if not quantity_text.isdigit() or int(quantity_text) <= 0:
            QMessageBox.warning(self, "Uyarı", "Geçerli bir miktar girin.")
            return

        quantity = int(quantity_text)
        for category, foods in self.food_data.items():
            if selected_food in foods:
                price = foods[selected_food]
                total_item_price = price * quantity
                delivery_time = self.get_delivery_time(selected_food)
                self.cart_items.append({"food": selected_food, "quantity": quantity, "price": price, "total": total_item_price, "delivery_time": delivery_time})
                self.cart_list.addItem(f"{selected_food} - {quantity} x {price} TL = {total_item_price} TL - Tahmini Teslimat: {delivery_time}")
                self.total_price += total_item_price
                self.update_total_label()
                return

    def get_delivery_time(self, food_name):
        delivery_times = {
            "Pizza": "30-40 dakika",
            "Burger": "20-30 dakika",
            "Pasta": "25-35 dakika",
            "Salata": "15-25 dakika",
            "Pide": "25-35 dakika",
            "Suşi": "40-50 dakika",
            "Kebap": "35-45 dakika",
            "Tavuk Sote": "20-30 dakika",
            "Mercimek Çorbası": "15-25 dakika",
            "Mantı": "30-40 dakika",
            "Izgara Somon": "45-55 dakika",
            "Köfte": "25-35 dakika",
            "Noodle": "20-30 dakika",
            "Tiramisu": "15-20 dakika",
            "Sütlaç": "10-15 dakika",
            "Su": "5-10 dakika",
            "Ayran": "5-10 dakika",
            "Kola": "5-10 dakika",
        }
        return delivery_times.get(food_name, "Tahmini teslimat süresi bulunamadı.")

    def update_total_label(self):
        self.total_label.setText(f"Toplam Tutar: {self.total_price} TL")

    def submit_order(self):
        if not self.cart_items:
            QMessageBox.warning(self, "Uyarı", "Sepetiniz boş!")
            return

        selected_address = self.address_combo.currentText()
        if selected_address == "Adres Seçin":
            QMessageBox.warning(self, "Uyarı", "Lütfen bir teslimat adresi seçin.")
            return

        order_details = {
            "user_phone": self.user_phone,
            "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": self.cart_items,
            "total_price": self.total_price,
            "delivery_address": selected_address
        }

        orders = read_json_file("orders.json", [])
        orders.append(order_details)
        write_json_file("orders.json", orders)

        QMessageBox.information(self, "Başarılı", f"Sipariş Verildi! Toplam Tutar: {self.total_price} TL\nTeslimat Adresi: {selected_address}")
        self.cart_list.clear()
        self.total_price = 0
        self.update_total_label()
        self.cart_items = []

class MyOrdersWindow(QMainWindow):
    def __init__(self, user_phone):
        super().__init__()
        self.setWindowTitle("Siparişlerim")
        self.setGeometry(100, 100, 400, 300)
        self.setObjectName("myOrdersWindow")
        self.user_phone = user_phone

        layout = QVBoxLayout()

        self.orders_list = QListWidget()
        layout.addWidget(self.orders_list)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.load_orders()

    def load_orders(self):
        self.orders_list.clear()
        orders = read_json_file("orders.json")
        user_orders = [order for order in orders if order["user_phone"] == self.user_phone]
        if user_orders:
            for order in user_orders:
                order_text = f"Sipariş Tarihi: {order['order_date']} - Toplam: {order['total_price']} TL\n"
                for item in order['items']:
                    order_text += f"  - {item['food']} ({item['quantity']} x {item['price']} TL) - Tahmini Teslimat: {item['delivery_time']}\n"  # Tahmini teslimat süresi eklendi
                order_text += f"  Teslimat Adresi: {order['delivery_address']}\n" # Teslimat adresi eklendi
                self.orders_list.addItem(order_text)
        else:
            self.orders_list.addItem("Henüz hiç siparişiniz bulunmamaktadır.")

class AccountWindow(QMainWindow):
    def __init__(self, name, phone, password):
        super().__init__()
        self.setWindowTitle("Hesap Bilgileri")
        self.setGeometry(100, 100, 400, 350)
        self.setObjectName("accountWindow")

        self.name = name
        self.phone = phone
        self.password = password

        layout = QVBoxLayout()

        self.name_label = QLabel(f"Ad Soyad: {self.name}")
        layout.addWidget(self.name_label)

        self.phone_label = QLabel(f"Telefon: {self.phone}")
        layout.addWidget(self.phone_label)

        self.addresses_label = QLabel("Kayıtlı Adresler:")
        layout.addWidget(self.addresses_label)

        self.addresses_list = QListWidget()
        self.load_addresses()
        layout.addWidget(self.addresses_list)

        add_address_button = QPushButton("Yeni Adres Ekle")
        add_address_button.clicked.connect(self.open_add_address_window)
        layout.addWidget(add_address_button)

        self.edit_button = QPushButton("Bilgileri Düzenle")
        self.edit_button.clicked.connect(self.edit_account_info)
        layout.addWidget(self.edit_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_addresses(self):
        """Kullanıcının adreslerini users.json dosyasından yükleyip listeye ekler."""
        self.addresses_list.clear()
        users = read_json_file("users.json")
        for user in users:
            if user["phone"] == self.phone:
                for address in user.get("addresses", []):
                    self.addresses_list.addItem(address)
                return

    def open_add_address_window(self):
        self.add_address_window = AddAddressWindow(self.phone)
        self.add_address_window.show()
        self.close()

    def edit_account_info(self):
        self.edit_window = EditAccountWindow(self.name, self.phone, self.password)
        self.edit_window.show()
        self.close()

class AddAddressWindow(QMainWindow):
    def __init__(self, user_phone):
        super().__init__()
        self.setWindowTitle("Yeni Adres Ekle")
        self.setGeometry(100, 100, 400, 150)
        self.setObjectName("addAddressWindow")
        self.user_phone = user_phone

        layout = QFormLayout()
        self.new_address_input = QLineEdit()
        self.new_address_input.setPlaceholderText("Yeni Adres")
        layout.addRow("Yeni Adres:", self.new_address_input)

        self.save_address_button = QPushButton("Kaydet")
        self.save_address_button.clicked.connect(self.save_new_address)
        layout.addWidget(self.save_address_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def save_new_address(self):
        new_address = self.new_address_input.text()
        if not new_address:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir adres girin.")
            return

        users = read_json_file("users.json")
        for user in users:
            if user["phone"] == self.user_phone:
                if "addresses" not in user:
                    user["addresses"] = []
                user["addresses"].append(new_address)
                break
        write_json_file("users.json", users)

        QMessageBox.information(self, "Başarılı", "Yeni adres eklendi.")
        self.account_window = AccountWindow("", self.user_phone, "")
        self.account_window.show()
        self.close()

class EditAccountWindow(QMainWindow):
    def __init__(self, name, phone, password):
        super().__init__()
        self.setWindowTitle("Hesap Bilgilerini Düzenle")
        self.setGeometry(100, 100, 400, 350)
        self.setObjectName("editAccountWindow")

        layout = QFormLayout()

        self.name_input = QLineEdit(name)
        layout.addRow("Ad Soyad:", self.name_input)

        self.phone_input = QLineEdit(phone)
        layout.addRow("Telefon:", self.phone_input)

        self.password_input = QLineEdit(password)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("Şifre:", self.password_input)

        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self.save_account_info)
        layout.addWidget(self.save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def save_account_info(self):
        new_name = self.name_input.text()
        new_phone = self.phone_input.text()
        new_password = self.password_input.text()

        users = read_json_file("users.json")
        for user in users:
            if user["phone"] == self.phone:
                user["name"] = new_name
                user["phone"] = new_phone
                # Şifreyi hashleyerek güncelle
                user["password"] = hash_password(new_password)
                break
        write_json_file("users.json", users)

        QMessageBox.information(self, "Bilgi", "Bilgiler güncellendi.")
        self.main_window = MainWindow(new_name, new_phone, new_password)
        self.main_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
