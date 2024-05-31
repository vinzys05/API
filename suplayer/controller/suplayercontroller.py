from config.database_config import DatabaseConnector
from suplayer.model.suplayermodels import Produk
from datetime import datetime,timedelta
import mysql.connector

class suplayercontroller:
    def __init__(self):
        self.db_connector = DatabaseConnector() 
        self.db = self.db_connector.connect_to_database()
        
    def get_all_produk(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("select * from suplayer")
            results = cursor.fetchall()
            cursor.close()
            
            produk_list = []
            for row in results:
                created_at = row['created_at']
                updated_at = row['updated_at']
                if isinstance(created_at, timedelta):
                    created_at = datetime.now() - created_at
                if isinstance(updated_at, timedelta): 
                    updated_at = datetime.now() - updated_at
                produk = Produk(row['id'], row['nama'], row['alamat'], row['telepon'], created_at, updated_at )
                produk_list.append(produk)
                
            return produk_list
        except mysql.connector.Error as e:
            print(f'Error: {e}')
            return 
        
    def lihat_produk(self):
        all_produk = self.get_all_produk()
        if all_produk is not None:
            produk_data = [produk.to_dict() for produk in all_produk]
            return {'produk': produk_data}, 200
        else:
            return {'massage': 'Terjadi kesalahan saat mengambil data produk'}, 500
            
    def cari_produk(self,id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("Select * from suplayer where id = %s", (id,))
            produk = cursor.fetchone()
            cursor.close()
            
            if produk:
                created_at = produk['created_at']
                updated_at = produk['updated_at']
                if isinstance(created_at, timedelta):
                    created_at = datetime.now() - created_at
                if isinstance(updated_at,timedelta):
                    updated_at = datetime.now() - updated_at
                produkobj = Produk(produk['id'],produk['nama'],produk['alamat'],produk['telepon'], created_at, updated_at)
                return {'pelangaan': produkobj.to_dict()}, 200
            else:
                return{'massage':'Data produk tidak ditemukan'}, 404
        except mysql.connector.Error as e:
            print(f'Error{e}')
            return{'massage': 'Terjadi kesalahan saat mencari data produk'}, 500
        
    def tambah_produk(self,data):
        try:
            nama = data.get('nama')
            alamat = data.get('alamat')
            telepon = data.get('telepon')
            created_at = datetime.now()
            updated_at = datetime.now()
            
            cursor = self.db.cursor()
            query ="insert into suplayer (nama, alamat, telepon, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query,(nama, alamat, telepon, created_at, updated_at))
            self.db.commit()
            cursor.close()
            
            return {'massagae': ' Data produk berhasil ditambahkan'}, 201 
        except mysql.connector.Error as e:
            print(f'Error:{e}')
            return{'massage': 'Terjadi kesalahan saat menambah data produk'}, 500
        
    def update_produk(self,id,data):
        try:
            if not data:
                return{'massage':'Data yang diterima kosong'}, 404
            
            cursor = self.db.cursor(dictionary=True)
            query = "Select * from produk where id_produk = %s"
            cursor.execute(query,(id,))
            produk = cursor.fetchone()
            cursor.close()
            
            if not produk:
                return{'massage': 'Data produk tidak ditemukan'}
            
            cursor = self.db.cursor()
            query = "update produk SET nama = %s , alamat = %s , telepon = %s , updated_at =NOW() where id_produk = %s"
            cursor.execute(query,(data['nama'], data['alamat'], data['telepon'], id))
            self.db.commit()
            cursor.close()
            
            return{'massage':'Data produk berhasil diperbarui'}, 200
        except mysql.connector.Error as e:
            print(f'Error: {e}')
            return{'massage':'Terjadi kesalahan saat memperbarui data produk'}, 500
        
    def hapus_produk(self,id):
        try:
            cursor = self.db.cursor()
            query = "delete from produk where id_produk = %s"
            cursor.execute(query,(id,))
            self.db.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                return{'massage':'Data produk berhasil di hapus'}, 200
            else:
                return{'massage':'Data produk tidak ditemukan'}, 404
        except mysql.connector.Error as e:
            print(f"Error:{e}")
            return{'massage': 'Terjadi kesalahan saat menghapus data produk'}, 500