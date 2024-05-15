from flask import Blueprint, request, jsonify
from produk.controller.pelanggancontroller import Pelanggancontroller

pelanggan_routes = Blueprint('pelanggan_routes',__name__)
pelanggan_controller = Pelanggancontroller()

@pelanggan_routes.route('/pelanggan', methods=['GET'])
def lihat_pelanggan():
        return jsonify(pelanggan_controller.lihat_pelanggan())
    
@pelanggan_routes.route('/pelangaan/<int:id>', methods =['GET'])
def cari_pelanggan(id):
    return pelanggan_controller.cari_pelanggan(id)

@pelanggan_routes.route('/pelanggan',methods=['POST'])
def tambah_pelanggan():
    data = request.json
    return pelanggan_controller.tambah_pelanggan(data)

@pelanggan_routes.route('/pelanggan/<int:id>', methods =['PUT'])
def update_pelanggan(id):
    data = request.json
    return pelanggan_controller.update_pelanggan(id,data)

@pelanggan_routes.route('/pelanggan/<int:id>', methods =['DELETE'])
def hapus_pealnggan(id):
    return pelanggan_controller.hapus_pelanggan(id)


    