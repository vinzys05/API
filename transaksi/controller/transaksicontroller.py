from config.database_config import DatabaseConnector
from transaksi.model.transaksimodels import Transaksi
from datetime import datetime,timedelta
import mysql.connector

class Transaksicontroller:
    def __init__(self):
        self.db_connector = DatabaseConnector() 
        self.db = self.db_connector.connect_to_database()
        
    def get_all_transaksi(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("select * from transaksi")
            results = cursor.fetchall()
            cursor.close()
            
            transaksi_list = []
            for row in results:
                created_at = row['created_at']
                updated_at = row['updated_at']
                if isinstance(created_at, timedelta):
                    created_at = datetime.now() - created_at
                if isinstance(updated_at, timedelta): 
                    updated_at = datetime.now() - updated_at
                transaksi = Transaksi(row['id_transaksi'],row['id_pelanggan'],row['tanggal'], created_at, updated_at)
                transaksi_list.append(transaksi)
                
            return transaksi_list
        except mysql.connector.Error as e:
            print(f"Error:{e}")
            return
        
    def lihat_transaksi(self):
        all_transaksi = self.get_all_transaksi()
        if all_transaksi is not None:
            transaksi_data = [transaksi.to_dict() for transaksi in all_transaksi]
            return {'produk': transaksi_data}, 200
        else:
            return {'massage':'Terjadi kesalahan saat mengambil data transaksi'}, 500
        
    def cari_transaksi(self,id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("Select * from transaksi where id_transaksi= %s", (id,))
            transaksi = cursor.fetchone()
            cursor.close()
            
            if transaksi:
                created_at = transaksi['created_at']
                updated_at = transaksi['updated_at']
                if isinstance(created_at, timedelta):
                    created_at = datetime.now() - created_at
                if isinstance(updated_at, timedelta): 
                    updated_at = datetime.now() - updated_at
                
                transaksiobj = Transaksi(transaksi['id_transaksi'],transaksi['id_pelanggan'],transaksi['tanggal'], created_at, updated_at)
                return {'transaksi': transaksiobj.to_dict()}, 200
            else:
                return{'massage':'Data transaksi tidak ditemukan'}, 404
        except mysql.connector.Error as e:
            print(f"Error{e}")
            return{'massage': 'Terjadi kesalahan saat mencari data transaksi'}, 500
        
    def tambah_transaksi(self,data):
        try:
            id_pelanggan = data.get('id_pelanggan')
            tanggal = data.get('tanggal')
            created_at = datetime.now()
            updated_at = datetime.now()
            
            cursor = self.db.cursor()
            query ="insert into transaksi (id_pelanggan, tanggal, created_at, updated_at) VALUES (%s, %s, %s, %s)"
            cursor.execute(query,(id_pelanggan, tanggal, created_at, updated_at))
            self.db.commit()
            cursor.close()
            
            return {'massagae': ' Data transaksi berhasil ditambahkan'}, 201 
        except mysql.connector.Error as e:
            print(f'Error:{e}')
            return{'massage': 'Terjadi kesalahan saat menambah data transaksi'}, 500
        
    def update_transaksi(self,id,data):
        try:
            if not data:
                return{'massage':'Data yang diterima kosong'}, 404
            
            cursor = self.db.cursor(dictionary=True)
            query = "Select * from transaksi where id_transaksi = %s"
            cursor.execute(query,(id,))
            pelanggan = cursor.fetchone()
            cursor.close()
            
            if not pelanggan:
                return{'massage': 'Data transaksi tidak ditemukan'}
            
            cursor = self.db.cursor()
            query = "update transaksi SET id_pelanggan = %s , tanggal = %s ,  updated_at =NOW() where id_transaksi = %s"
            cursor.execute(query,(data['id_pelanggan'], data['tanggal'],  id))
            self.db.commit()
            cursor.close()
            
            return{'massage':'Data transaksi berhasil diperbarui'}, 200
        except mysql.connector.Error as e:
            print(f'Error: {e}')
            return{'massage':'Terjadi kesalahan saat memperbarui data transaksi'}, 500
        
    def hapus_transaksi(self,id):
        try:
            cursor = self.db.cursor()
            query = "delete from transaksi where id_transaksi = %s"
            cursor.execute(query,(id,))
            self.db.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                return{'massage':'Data transaksi berhasil di hapus'}, 200
            else:
                return{'massage':'Data transaksi tidak ditemukan'}, 404
        except mysql.connector.Error as e:
            print(f"Error:{e}")
            return{'massage': 'Terjadi kesalahan saat menghapus data transaksi'}, 500