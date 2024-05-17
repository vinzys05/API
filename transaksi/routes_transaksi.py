from flask import Blueprint,request,jsonify
from transaksi.controller.transaksicontroller import Transaksicontroller

transaksi_routes = Blueprint('transaksi_routes',__name__)
transaksi_controller = Transaksicontroller()

@transaksi_routes.route('/transaksi',methods=['GET'])
def lihat_transaksi():
    if request.method == 'GET':
        return jsonify(transaksi_controller.lihat_transaksi())
    
@transaksi_routes.route('/transaksi/<int:id>',methods=['GET'])
def cari_transaksi(id):
    return transaksi_controller.cari_transaksi(id)

@transaksi_routes.route('/transaksi',methods=['POST'])
def tambah_transaksi():
    data = request.json
    return transaksi_controller.tambah_transaksi(data)

@transaksi_routes.route('/transaksi/<int:id>',methods=['PUT'])
def update_transaksi(id):
    data = request.json
    return transaksi_controller.update_transaksi(id,data)

#@transaksi_routes.route('/transaksi/<int:id>',methods=['DELETE'])
#def hapus_transaksi(id):
#    return transaksi_controller.hapus_transaksi(id)