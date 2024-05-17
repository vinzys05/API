from flask import Blueprint,request,jsonify
from detail_transaksi.controller.detailcontroller import Detailcontroller

detail_routes = Blueprint('detail_routes',__name__)
detail_controller = Detailcontroller()

@detail_routes.route('/detail',methods=['GET'])
def lihat_detailtransaksi():
    if request.method == 'GET':
        return jsonify(detail_controller.lihat_detailtransaksi())
    
@detail_routes.route('/detail/<int:id>',methods=['GET'])
def cari_detailtransaksi(id):
    return detail_controller.cari_detailtransaksi(id)

@detail_routes.route('/detail',methods= ['POST'])
def tambah_detailtransaksi():
    data = request.json
    return detail_controller.tambah_detailtransaksi(data)

@detail_routes.route('/detail/<int:id>', methods=['PUT'])
def update_detailtransaksi(id):
    data = request.json
    return detail_controller.update_detailtransaksi(id,data)

@detail_routes.route('/detail/<int:id>', methods=['DELETE'])
def hapus_detailtransaksi(id):
    return detail_controller.hapus_detailtransaksi(id)