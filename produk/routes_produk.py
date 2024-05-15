from flask import Blueprint, request, jsonify
from produk.controller.produkcontroller import ProdukController

produk_routes = Blueprint('produk_routes', __name__)
produk_controller = ProdukController()

@produk_routes.route('/produk', methods=['GET'])
def lihat_produk():
    if request.method == 'GET':
        return jsonify(produk_controller.lihat_produk())
    
@produk_routes.route('/produk/<int:id>', methods=['GET'])
def cari_produk(id):
    return produk_controller.cari_produk(id)

@produk_routes.route('/produk',methods=['POST'])
def tambah_produk():
    data = request.json
    return produk_controller.tambah_produk(data)

@produk_routes.route('/produk/<int:id>',methods= ['PUT'])
def update_produk(id):
    data = request.json
    return produk_controller.update_produk(id,data)

@produk_routes.route('/produk/<int:id>', methods=['DELETE'])
def hapus_produk(id):
    return produk_controller.hapus_produk(id)