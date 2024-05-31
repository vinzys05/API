from flask import Blueprint, request, jsonify
from suplayer.controller.suplayercontroller import suplayercontroller

suplayer_routes = Blueprint('suplayer_routes', __name__)
produk_controller = suplayercontroller()

@suplayer_routes.route('/suplayer', methods=['GET'])
def lihat_produk():
    if request.method == 'GET':
        return jsonify(produk_controller.lihat_produk())
    
@suplayer_routes.route('/suplayer/<int:id>', methods=['GET'])
def cari_produk(id):
    return produk_controller.cari_produk(id)

@suplayer_routes.route('/suplayer',methods=['POST'])
def tambah_produk():
    data = request.json
    return produk_controller.tambah_produk(data)

@suplayer_routes.route('/produk/<int:id>',methods= ['PUT'])
def update_produk(id):
    data = request.json
    return produk_controller.update_produk(id,data)

@suplayer_routes.route('/produk/<int:id>', methods=['DELETE'])
def hapus_produk(id):
    return produk_controller.hapus_produk(id)