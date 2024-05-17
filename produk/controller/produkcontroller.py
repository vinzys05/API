from config.database_config import DatabaseConnector 
from produk.model.produkmodels import Produk
from datetime import datetime, timedelta
import mysql.connector

class ProdukController:
    def __init__(self):
        self.db_connector = DatabaseConnector() 
        self.db = self.db_connector.connect_to_database()
        
    def get_all_produk(self):
        try:
            cursor =self.db.cursor(dictionary=True)
            cursor.execute("select * from produk")
            results = cursor.fetchall()
            cursor.close()
            
            produk_list=[] 
            for produk in results:
                
                created_at = produk['created_at']
                updated_at = produk['updated_at']
                if isinstance(created_at, timedelta):
                    created_at = datetime.now() - created_at
                if isinstance(updated_at, timedelta): 
                    updated_at = datetime.now() - updated_at
                produk = Produk(produk['id_produk'], produk['nama'], produk['kategori'], produk['harga'], produk['stok'], created_at, updated_at) 
                produk_list.append(produk)
            
            return produk_list
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return
        
     # melihat dengan json
    def lihat_produk(self):
        all_produk = self.get_all_produk()
        if all_produk is not None:
            produk_data = [produk.to_dict() for produk in all_produk]
            return {'produk': produk_data}, 200
        else:
            return {'message': 'Terjadi kesalahan saat mengambil data produk'}, 500
        
    def cari_produk(self,id):
        try:
            cursor =self.db.cursor(dictionary=True)
            cursor.execute("select * from produk where id_produk = %s", (id,))
            produk = cursor.fetchone()
            cursor.close()
            
            if produk:
                created_at = produk['created_at']
                updated_at = produk['updated_at']
                if isinstance(created_at, timedelta):
                    created_at = datetime.now() - created_at
                if isinstance(updated_at, timedelta): 
                    updated_at = datetime.now() - updated_at
                produkobj = Produk(produk['id_produk'], produk['nama'], produk['kategori'], produk['harga'], produk['stok'], created_at, updated_at) 
                return {'produk': produkobj.to_dict()}, 200
            else:
                return {'massage': 'Data produk tidak ditemukan'}, 404
        except mysql.connector.Error as e:
            print(f"Error:{e}")
            return{'massage': 'Terjadi kesalahan saat mencari data produk '}, 500
        
    def tambah_produk(self,data):
        try:
            nama = data.get('nama')
            kategori = data.get('kategori')
            harga = data.get('harga')
            stok = data.get('stok')
            created_at = datetime.now()
            updated_at = datetime.now()
            
            cursor = self.db.cursor()
            query = "insert into produk (nama, kategori, harga, stok, created_at, updated_at ) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (nama, kategori, harga, stok, created_at, updated_at))
            self.db.commit()
            cursor.close()
            
            return {'massage': 'Data produk telah ditambahkan'}, 201
        except mysql.connector.Error as e:
            print(f"Error:{e}")
            return{'massage': 'Terjadi kesalahan saat menambahkan data produk '}, 500
        
    def update_produk(self,id,data):
        try:
            if not data:
                return {'massage' : 'Data yang diterima kosong'}, 400
            
            cursor = self.db.cursor(dictionary=True)
            query = "select * from produk where id_produk = %s"
            cursor.execute(query, (id,))
            guru = cursor.fetchone()
            cursor.close()
            
            if not guru:
                return{'massage' : 'Data produk tidak ditemukan'}, 404
            
            cursor = self.db.cursor()
            query = "update produk SET nama = %s, kategori = %s, harga = %s, stok = %s,  updated_at = NOW() where id_produk = %s"
            cursor.execute(query, (data['nama'], data['kategori'], data['harga'], data['stok'], id))
            self.db.commit()
            cursor.close()
            
            return {'masssage':'Data berhasil diperbarui'}, 200
        except mysql.connector.Error as e:
            print (f"Error: {e}")
            return{'massage':'Terjadi kesalahan saat memperbarui data produk'}, 500
        
    def hapus_produk(self,id):
        try:
            cursor = self.db.cursor()
            query = "delete from produk where id_produk = %s"
            cursor.execute(query, (id,))
            self.db.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                return{'massage':'Data produk bershasil di hapus'}, 200
            else:
                return{'massage':'Data produk tidak ditemukan'}, 404
        except mysql.connector.Error as e:
            print(f'Error: {e}')
            return{'massage': 'Terjadi kesalahan saat menghapus data produk'}, 500