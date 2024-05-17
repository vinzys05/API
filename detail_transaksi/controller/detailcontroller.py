from config.database_config import DatabaseConnector
from detail_transaksi.model.detailmodels import Detailtransaksi
from datetime import datetime, timedelta
import mysql.connector

class Detailcontroller:
    def __init__(self):
        self.db_connector = DatabaseConnector() 
        self.db = self.db_connector.connect_to_database()
        
    def get_all_Detailtransaksi(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("select * from detail_transaksi")
            results = cursor.fetchall()
            cursor.close()
            
            detailtransaksi_list = []
            for row in results:
                created_at = row['created_at']
                updated_at = row['updated_at']
                if isinstance(created_at, timedelta):
                    created_at = datetime.now() - created_at
                if isinstance(updated_at, timedelta): 
                    updated_at = datetime.now() - updated_at
                detailtransaksi = Detailtransaksi(row['id_detail'],row['id_transaksi'],row['id_produk'],row['jumlah'],row['harga'],row['total'],row['sub_total'],row['metode_pembayaran'], created_at, updated_at)
                detailtransaksi_list.append(detailtransaksi)
                
            return detailtransaksi_list
        except mysql.connector.Error as e:
            print(f"Error:{e}")
            return
        
    def lihat_detailtransaksi(self):
        all_detailtransaksi = self.get_all_Detailtransaksi()
        if all_detailtransaksi is not None:
            detailtransaksi_data = [detailtransaksi.to_dict() for detailtransaksi in all_detailtransaksi]
            return {'Detail transaksi': detailtransaksi_data}, 200
        else:
            return {'massage':'Terjadi kesalahan saat mengambil data detail detailtransaksi'}, 500
        
    def cari_detailtransaksi(self,id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("Select * from detail_transaksi where id_detail= %s", (id,))
            detailtransaksi = cursor.fetchone()
            cursor.close()
            
            if detailtransaksi:
                created_at = detailtransaksi['created_at']
                updated_at = detailtransaksi['updated_at']
                if isinstance(created_at, timedelta):
                    created_at = datetime.now() - created_at
                if isinstance(updated_at, timedelta): 
                    updated_at = datetime.now() - updated_at
                
                detailtransaksiobj = Detailtransaksi(detailtransaksi['id_detail'],detailtransaksi['id_transaksi'],detailtransaksi['id_produk'],detailtransaksi['jumlah'],detailtransaksi['harga'],detailtransaksi['total'],detailtransaksi['sub_total'],detailtransaksi['metode_pembayaran'], created_at, updated_at)
                return {'Detail transaksi': detailtransaksiobj.to_dict()}, 200
            else:
                return {'massage':'Data detail transaksi tidak ditemukan'}
        except mysql.connector.Error as e:
            print(f'Error:{e}')
            return {'massage':'Terjadi kesalahan saat mencari data detail transaksi'}, 500
        
    def tambah_detailtransaksi(self,data):
        try:
            id_detail = data.get('id_detail')
            id_transaksi = data.get('id_transaksi')
            id_produk = data.get('id_produk')
            jumlah = data.get('jumlah')
            harga = data.get('harga')
            total = data.get('total')
            sub_total = data.get('sub_total')
            metode_pembayaran = data.get('metode_pembayaran')
            created_at = datetime.now()
            updated_at = datetime.now()
            
            cursor = self.db.cursor()
            query ="insert into detail_transaksi (id_detail, id_transaksi, id_produk, jumlah, harga, total, sub_total, metode_pembayaran, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query,(id_detail, id_transaksi, id_produk, jumlah, harga, total, sub_total, metode_pembayaran, created_at, updated_at))
            self.db.commit()
            cursor.close()
            
            return {'massagae': ' Data detail transaksi berhasil ditambahkan'}, 201 
        except mysql.connector.Error as e:
            print(f'Error:{e}')
            return{'massage': 'Terjadi kesalahan saat menambah data detail transaksi'}, 500
        
    def update_detailtransaksi(self,id,data):
        try:
            if not data:
                return{'massage':'Data yang diterima kosong'}, 404
            
            cursor = self.db.cursor(dictionary=True)
            query = "Select * from detail_transaksi where id_detail = %s"
            cursor.execute(query,(id,))
            detailtransaksi = cursor.fetchone()
            cursor.close()
            
            if not detailtransaksi:
                return{'massage': 'Data detail transaksi tidak ditemukan'}
            
            cursor = self.db.cursor()
            query = "update detail_transaksi SET id_transaksi = %s , id_produk = %s , jumlah = %s , harga = %s , total = %s , sub_total = %s , metode_pembayaran = %s , updated_at =NOW() where id_detail = %s"
            cursor.execute(query,(data['id_transaksi'],data['id_produk'],data['jumlah'],data['harga'],data['total'],data['sub_total'],data['metode_pembayaran'], id))
            self.db.commit()
            cursor.close()
            
            return{'massage':'Data detail transaksi berhasil diperbarui'}, 200
        except mysql.connector.Error as e:
            print(f'Error: {e}')
            return{'massage':'Terjadi kesalahan saat memperbarui data detail transaksi'}, 500
        
    def hapus_detailtransaksi(self,id):
        try:
            cursor = self.db.cursor()
            query = "delete from detail_transaksi where id_detail = %s"
            cursor.execute(query,(id,))
            self.db.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                return{'massage':'Data detail transaksi berhasil di hapus'}, 200
            else:
                return{'massage':'Data detail transaksi tidak ditemukan'}, 404
        except mysql.connector.Error as e:
            print(f"Error:{e}")
            return{'massage': 'Terjadi kesalahan saat menghapus data detail transaksi'}, 500