from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 设置一个安全的密钥
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)

# 仓库模型
class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
#入库材料信息
class StockInForm(FlaskForm):
    material_id = StringField('材料编号', validators=[DataRequired()])
    name = StringField('材料名称', validators=[DataRequired()])
    quantity = IntegerField('入库数量', validators=[DataRequired(), NumberRange(min=1)])
    date = DateField('入库日期', validators=[DataRequired()])
    location = SelectField('存放地点', choices=[
        ('', '选择存放地点'),
        ('仓库A-01区', '仓库A-01区'),
        ('仓库A-02区', '仓库A-02区'),
        ('仓库B-01区', '仓库B-01区'),
        ('仓库B-02区', '仓库B-02区')
    ], validators=[DataRequired()])
    supplier = StringField('供应商')
    purchase_order = StringField('采购单号')
    status = SelectField('质检状态', choices=[
        ('', '选择质检状态'),
        ('合格', '合格'),
        ('不合格', '不合格'),
        ('待检', '待检')
    ], validators=[DataRequired()])
    notes = TextAreaField('备注')

@app.route('/')
def home():
    logging.debug("访问首页")
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
    logging.debug("访问库存管理页面")
    return render_template('inventory/inventory.html', title='库存管理')

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

@app.route('/settings/users')
def settings_users():
    return render_template('settings/settings_users.html', title='用户管理')

@app.route('/settings/permissions')
def settings_permissions():
    return render_template('settings/settings_permissions.html', title='权限管理')

@app.route('/settings/logs')
def settings_logs():
    return render_template('settings/settings_logs.html', title='日志管理')

@app.route('/settings/config')
def settings_config():
    return render_template('settings/settings_config.html', title='系统配置')

@app.route('/inventory/stock-in', methods=['GET', 'POST'])
def stock_in():
    form = StockInForm()
    if form.validate_on_submit():
        try:
            # 获取表单数据
            material_id = form.material_id.data
            name = form.name.data
            quantity = form.quantity.data
            date = form.date.data
            location = form.location.data
            supplier = form.supplier.data
            purchase_order = form.purchase_order.data
            status = form.status.data
            notes = form.notes.data

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
    
    return render_template('inventory/inventory_stock_in.html', form=form)

@app.route('/inventory/stock-out')
def stock_out():
    return render_template('inventory/inventory_stock_out.html', title='出库管理')

@app.route('/inventory/query')
def inventory_query():
    return render_template('inventory/inventory_query.html', title='库存查询')

@app.route('/inventory/transfer')
def inventory_transfer():
    return render_template('inventory/inventory_transfer.html', title='库存调拨')

@app.route('/inventory/check')
def inventory_check():
    return render_template('inventory_check.html', title='库存盘点')

@app.route('/inventory/alert')
def inventory_alert():
    return render_template('inventory_alert.html', title='库存预警')

@app.route('/inventory/batch')
def inventory_batch():
    return render_template('inventory/inventory_batch.html', title='批次管理')

@app.route('/inventory/analysis')
def inventory_analysis():
    return render_template('inventory_analysis.html', title='库存分析')

@app.route('/inventory/return')
def inventory_return():
    return render_template('inventory/inventory_return.html', title='退货管理')

@app.route('/inventory/warehouse', methods=['GET', 'POST'])
def inventory_warehouse():
    if request.method == 'POST':
        # 处理添加仓库请求
        name = request.form.get('name')
        location = request.form.get('location')
        capacity_str = request.form.get('capacity')
        try:
            capacity = int(capacity_str)
            if not all([name, location, capacity]):
                flash('请填写所有必填项', 'error')
            else:
                new_warehouse = Warehouse(name=name, location=location, capacity=capacity)
                db.session.add(new_warehouse)
                db.session.commit()
                flash('仓库添加成功', 'success')
        except ValueError:
            flash('仓库容量必须是整数', 'error')
        except Exception as e:
            flash(f'仓库添加失败: {str(e)}', 'error')
            app.logger.error(f'添加仓库失败: {str(e)}', exc_info=True)

        return redirect(url_for('inventory_warehouse'))

    # 获取所有仓库信息
    warehouses = Warehouse.query.all()
    return render_template('inventory/inventory_warehouse.html', warehouses=warehouses)

@app.route('/inventory/warehouse/edit/<int:id>', methods=['GET', 'POST'])
def edit_warehouse(id):
    warehouse = Warehouse.query.get_or_404(id)

    if request.method == 'POST':
        # 处理编辑仓库请求
        name = request.form.get('name')
        location = request.form.get('location')
        capacity_str = request.form.get('capacity')
        try:
            capacity = int(capacity_str)
            if not all([name, location, capacity]):
                flash('请填写所有必填项', 'error')
            else:
                warehouse.name = name
                warehouse.location = location
                warehouse.capacity = capacity
                db.session.commit()
                flash('仓库信息更新成功', 'success')
        except ValueError:
            flash('仓库容量必须是整数', 'error')
        except Exception as e:
            flash(f'仓库信息更新失败: {str(e)}', 'error')
            app.logger.error(f'更新仓库信息失败: {str(e)}', exc_info=True)

        return redirect(url_for('inventory_warehouse'))

    return render_template('inventory/inventory_edit_warehouse.html', warehouse=warehouse)

@app.route('/inventory/warehouse/delete/<int:id>')
def delete_warehouse(id):
    try:
        warehouse = Warehouse.query.get_or_404(id)
        db.session.delete(warehouse)
        db.session.commit()
        flash('仓库删除成功', 'success')
    except Exception as e:
        flash(f'仓库删除失败: {str(e)}', 'error')
        app.logger.error(f'删除仓库失败: {str(e)}', exc_info=True)
    return redirect(url_for('inventory_warehouse'))

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
    return render_template('inventory/inventory_material_edit.html', material_id=material_id)

@app.route('/inventory/material/delete/<material_id>', methods=['DELETE'])
def delete_material(material_id):
    # 执行删除操作
    try:
        # 这里添加实际的删除逻辑
        return '', 204
    except Exception as e:
        app.logger.error(f'删除材料失败: {str(e)}', exc_info=True)
        return str(e), 500

@app.route('/inventory/material/update/<material_id>', methods=['PUT'])
def update_material(material_id):
    try:
        data = request.get_json()
        required_fields = ['name', 'category', 'quantity', 'unit', 'location', 'date', 'status']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'缺少必要字段: {field}')

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
    except ValueError as e:
        app.logger.error(f'更新材料信息失败: {str(e)}', exc_info=True)
        return str(e), 400
    except Exception as e:
        app.logger.error(f'更新材料信息失败: {str(e)}', exc_info=True)
        return str(e), 500

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    results = []

    if query:
        # 示例搜索逻辑，实际应根据需求扩展
        # 搜索仓库
        warehouse_results = Warehouse.query.filter(
            (Warehouse.name.contains(query)) |
            (Warehouse.location.contains(query))
        ).all()
        for warehouse in warehouse_results:
            results.append({
                'type': '仓库',
                'name': warehouse.name,
                'url': url_for('inventory_warehouse')
            })

        # 搜索其他模块（可根据需要扩展）
        # ...

    return render_template('search_results.html', query=query, results=results)

@app.route('/search/suggest')
def search_suggest():
    query = request.args.get('q', '').strip()
    results = []

    if query:
        # 搜索仓库
        warehouse_results = Warehouse.query.filter(
            (Warehouse.name.contains(query)) |
            (Warehouse.location.contains(query))
        ).all()
        for warehouse in warehouse_results:
            results.append({
                'type': '仓库',
                'name': warehouse.name,
                'url': url_for('inventory_warehouse')
            })

        # 搜索其他模块（可根据需要扩展）
        # 例如：搜索材料、商品等
        # ...

    return jsonify(results)

@app.route('/inventory/item/edit/<item_id>')
def edit_item(item_id):
    return render_template('inventory/inventory_item_edit.html', item_id=item_id)

@app.route('/inventory/system')
def inventory_system():
    return render_template('inventory/inventory_system.html', title='库存系统管理')

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()  # 创建所有表

        # 启动 Flask 应用
        app.run(debug=True, port=5000)
    except SystemExit as e:
        app.logger.error(f'应用启动时发生 SystemExit 异常: {str(e)}', exc_info=True)
    except Exception as e:
        app.logger.error(f'应用启动时发生异常: {str(e)}', exc_info=True)
