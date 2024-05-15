from config.database_config import DatabaseConnector
from produk.model.pelangganmodels import Pelanggan
from datetime import datetime,timedelta
import mysql.connector

class Pelanggancontroller:
    def __init__(self):
        self.db_connector = DatabaseConnector() 
        self.db = self.db_connector.connect_to_database()
        
    def get_all_pelanggan(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("select * from pelanggan")
            results = cursor.fetchall()
            cursor.close()
            
            pelanggan_list = []
            for row in results:
                created_at = row['created_at']
                updated_at = row['updated_at']
                if isinstance(created_at, timedelta):
                    created_at = datetime.now() - created_at
                if isinstance(updated_at, timedelta): 
                    updated_at = datetime.now() - updated_at
                pelanggan = Pelanggan(row['id_pelanggan'], row['nama'], row['alamat'], row['telepon'], created_at, updated_at )
                pelanggan_list.append(pelanggan)
                
            return pelanggan_list
        except mysql.connector.Error as e:
            print(f'Error: {e}')
            return 
        
    def lihat_pelanggan(self):
        all_pelanggan = self.get_all_pelanggan()
        if all_pelanggan is not None:
            pelanggan_data = [pelanggan.to_dict() for pelanggan in all_pelanggan]
            return {'Pelanggan': pelanggan_data}, 200
        else:
            return {'massage': 'Terjadi kesalahan saat mengambil data pelanggan'}, 500
            
    def cari_pelanggan(self,id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("Select * from pelanggan where id_pelanggan = %s", (id,))
            pelanggan = cursor.fetchone()
            cursor.close()
            
            if pelanggan:
                created_at = pelanggan['created_at']
                updated_at = pelanggan['updated_at']
                if isinstance(created_at, timedelta):
                    created_at = datetime.now() - created_at
                if isinstance(updated_at,timedelta):
                    updated_at = datetime.now() - updated_at
                pelangganobj = Pelanggan(pelanggan['id_pelanggan'],pelanggan['nama'],pelanggan['alamat'],pelanggan['telepon'], created_at, updated_at)
                return {'pelangaan': pelangganobj.to_dict()}, 200
            else:
                return{'massage':'Data pelanggan tidak ditemukan'}, 404
        except mysql.connector.Error as e:
            print(f'Error{e}')
            return{'massage': 'Terjadi kesalahan saat mencari data pelanggan'}, 500
        
    def tambah_pelanggan(self,data):
        try:
            nama = data.get('nama')
            alamat = data.get('alamat')
            telepon = data.get('telepon')
            created_at = datetime.now()
            updated_at = datetime.now()
            
            cursor = self.db.cursor()
            query ="insert into pelanggan (nama, alamat, telepon, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query,(nama, alamat, telepon, created_at, updated_at))
            self.db.commit()
            cursor.close()
            
            return {'massagae': ' Data pelanggan berhasil ditambahkan'}, 201 
        except mysql.connector.Error as e:
            print(f'Error:{e}')
            return{'massage': 'Terjadi kesalahan saat menambah data pelanggan'}, 500
        
    def update_pelanggan(self,id,data):
        try:
            if not data:
                return{'massage':'Data yang diterima kosong'},404
            
            cursor = self.db.cursor(dictionary=True)
            query = "Select * from pelanggan where id_pelanggan = %s"
            cursor.execute(query,(id,))
            pelanggan = cursor.fetchone()
            cursor.close()
            
            if not pelanggan:
                return{'massage': 'Data pelanggan tidak ditemukan'}
            
            cursor = self.db.cursor()
            query = "update pelanggan SET nama = %s , alamat = %s , telepon = %s , updated_at =NOW() where id_pelanggan = %s"
            cursor.execute(query,(data['nama'], data['alamat'], data['telepon'], id))
            self.db.commit()
            cursor.close()
            
            return{'massage':'Data pelanggan berhasil diperbarui'}, 200
        except mysql.connector.Error as e:
            print(f'Error: {e}')
            return{'massage':'Terjadi kesalahan saat memperbarui data pelanggan'}, 500
        
    def hapus_pelanggan(self,id):
        try:
            cursor = self.db.cursor()
            query = " Delete from pelanggan where id_pelanggan = %s"
            cursor.execute(query,(id,))
            self.db.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                return{'massage':'Data pelanggan berhasil di hapus'}, 200
            else:
                return{'massage':'Data pelanggan tidak ditemukan'}, 404
        except mysql.connector.Error as e:
            print(f"Error:{e}")
            return{'massage': 'Terjadi kesalahan saat menghapus data pelanggan'}, 500