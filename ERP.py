from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 设置一个安全的密钥
csrf = CSRFProtect(app)

@app.route('/')
def home():
    # 定义导航菜单项
    nav_items = [
        {'name': '销售管理', 'url': '/sales'},
        {'name': '采购管理', 'url': '/purchase'},
        {'name': '库存管理', 'url': '/inventory'},
        {'name': '财务管理', 'url': '/finance'},
        {'name': '人力资源管理', 'url': '/hr'},
        {'name': '生产管理', 'url': '/production'},
        {'name': '系统设置', 'url': '/settings'}
    ]
    return render_template('home.html', nav_items=nav_items)

# 添加二级页面路由
@app.route('/sales')
def sales():
    return render_template('sales.html', title='销售管理')

@app.route('/purchase')
def purchase():
    return render_template('purchase.html', title='采购管理')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html', title='库存管理')

@app.route('/finance')
def finance():
    return render_template('finance.html', title='财务管理')

@app.route('/hr')
def hr():
    return render_template('hr.html', title='人力资源管理')

@app.route('/production')
def production():
    return render_template('production.html', title='生产管理')

@app.route('/settings')
def settings():
    return render_template('settings.html', title='系统设置')

@app.route('/inventory/stock-in', methods=['GET', 'POST'])
def stock_in():
    if request.method == 'POST':
        try:
            # 获取表单数据
            material_id = request.form.get('material_id')
            name = request.form.get('name')
            quantity = int(request.form.get('quantity'))
            date = request.form.get('date')
            location = request.form.get('location')
            supplier = request.form.get('supplier')
            purchase_order = request.form.get('purchase_order')
            status = request.form.get('status')
            notes = request.form.get('notes')

            # 数据验证
            if not all([material_id, name, quantity, date, location, status]):
                raise ValueError('请填写所有必填项')

            if quantity <= 0:
                raise ValueError('入库数量必须大于0')

            # 这里添加实际的入库逻辑
            # 例如：将数据保存到数据库
            # db.session.add(new_stock)
            # db.session.commit()

            flash('材料入库成功', 'success')
            return redirect(url_for('stock_in'))

        except ValueError as e:
            flash(f'数据验证失败: {str(e)}', 'error')
        except Exception as e:
            flash(f'材料入库失败: {str(e)}', 'error')
            app.logger.error(f'入库失败: {str(e)}', exc_info=True)
        
        return redirect(url_for('stock_in'))
    
    return render_template('stock_in.html', title='入库管理')

@app.route('/inventory/stock-out')
def stock_out():
    return render_template('stock_out.html', title='出库管理')

@app.route('/inventory/query')
def inventory_query():
    return render_template('inventory_query.html', title='库存查询')

@app.route('/inventory/transfer')
def inventory_transfer():
    return render_template('inventory_transfer.html', title='库存调拨')

@app.route('/inventory/check')
def inventory_check():
    return render_template('inventory_check.html', title='库存盘点')

@app.route('/inventory/alert')
def inventory_alert():
    return render_template('inventory_alert.html', title='库存预警')

@app.route('/inventory/batch')
def inventory_batch():
    return render_template('inventory_batch.html', title='批次管理')

@app.route('/inventory/analysis')
def inventory_analysis():
    return render_template('inventory_analysis.html', title='库存分析')

@app.route('/inventory/return')
def inventory_return():
    return render_template('inventory_return.html', title='退货管理')

@app.route('/inventory/warehouse')
def inventory_warehouse():
    return render_template('inventory_warehouse.html', title='仓库管理')

@app.route('/inventory/cost')
def inventory_cost():
    return render_template('inventory_cost.html', title='库存成本')

@app.route('/inventory/expiring')
def inventory_expiring():
    return render_template('inventory_expiring.html', title='临期管理')

@app.route('/inventory/forecast')
def inventory_forecast():
    return render_template('inventory_forecast.html', title='库存预测')

@app.route('/inventory/barcode')
def inventory_barcode():
    return render_template('inventory_barcode.html', title='条码管理')

@app.route('/inventory/material/edit/<material_id>')
def edit_material(material_id):
    # 获取材料信息并渲染编辑页面
    return render_template('material_edit.html', material_id=material_id)

@app.route('/inventory/material/delete/<material_id>', methods=['DELETE'])
def delete_material(material_id):
    # 执行删除操作
    try:
        # 这里添加实际的删除逻辑
        return '', 204
    except Exception as e:
        return str(e), 500

@app.route('/inventory/material/update/<material_id>', methods=['PUT'])
def update_material(material_id):
    try:
        data = request.get_json()
        # 这里添加实际的更新逻辑
        # 例如：更新数据库中的材料信息
        # 返回更新后的数据
        return jsonify({
            'material_id': material_id,
            'name': data['name'],
            'category': data['category'],
            'quantity': data['quantity'],
            'unit': data['unit'],
            'location': data['location'],
            'date': data['date'],
            'status': data['status']
        }), 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)