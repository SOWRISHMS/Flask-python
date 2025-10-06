from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import db, init_db
from models import Product, Location, ProductMovement
from sqlalchemy import func
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

@app.route('/')
def index():
    return render_template('base.html')

# Product Routes
@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        description = request.form['description']
        
        if Product.query.get(product_id):
            flash('Product ID already exists!', 'error')
            return redirect(url_for('add_product'))
        
        new_product = Product(product_id=product_id, name=name, description=description)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('add_edit_forms.html', type='product', action='Add')

@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('add_edit_forms.html', type='product', action='Edit', item=product)

@app.route('/delete_product/<product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))

# Location Routes
@app.route('/locations')
def locations():
    all_locations = Location.query.all()
    return render_template('locations.html', locations=all_locations)

@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location_id = request.form['location_id']
        name = request.form['name']
        address = request.form['address']
        
        if Location.query.get(location_id):
            flash('Location ID already exists!', 'error')
            return redirect(url_for('add_location'))
        
        new_location = Location(location_id=location_id, name=name, address=address)
        db.session.add(new_location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('add_edit_forms.html', type='location', action='Add')

@app.route('/edit_location/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    if request.method == 'POST':
        location.name = request.form['name']
        location.address = request.form['address']
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('add_edit_forms.html', type='location', action='Edit', item=location)

@app.route('/delete_location/<location_id>')
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('locations'))

# Product Movement Routes
@app.route('/movements')
def movements():
    all_movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=all_movements)

@app.route('/add_movement', methods=['GET', 'POST'])
def add_movement():
    products = Product.query.all()
    locations = Location.query.all()
    
    if request.method == 'POST':
        movement_id = f"MOV_{uuid.uuid4().hex[:8].upper()}"
        from_location = request.form['from_location'] if request.form['from_location'] else None
        to_location = request.form['to_location'] if request.form['to_location'] else None
        product_id = request.form['product_id']
        qty = int(request.form['qty'])
        
        # Validate that both from and to locations are not the same
        if from_location and to_location and from_location == to_location:
            flash('From and To locations cannot be the same!', 'error')
            return redirect(url_for('add_movement'))
        
        # Validate that at least one location is provided
        if not from_location and not to_location:
            flash('Either From Location or To Location must be provided!', 'error')
            return redirect(url_for('add_movement'))
        
        new_movement = ProductMovement(
            movement_id=movement_id,
            from_location=from_location,
            to_location=to_location,
            product_id=product_id,
            qty=qty
        )
        
        db.session.add(new_movement)
        db.session.commit()
        flash('Product movement added successfully!', 'success')
        return redirect(url_for('movements'))
    
    return render_template('add_edit_forms.html', type='movement', action='Add', 
                          products=products, locations=locations)

@app.route('/edit_movement/<movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    products = Product.query.all()
    locations = Location.query.all()
    
    if request.method == 'POST':
        from_location = request.form['from_location'] if request.form['from_location'] else None
        to_location = request.form['to_location'] if request.form['to_location'] else None
        product_id = request.form['product_id']
        qty = int(request.form['qty'])
        
        # Validate that both from and to locations are not the same
        if from_location and to_location and from_location == to_location:
            flash('From and To locations cannot be the same!', 'error')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        
        # Validate that at least one location is provided
        if not from_location and not to_location:
            flash('Either From Location or To Location must be provided!', 'error')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        
        movement.from_location = from_location
        movement.to_location = to_location
        movement.product_id = product_id
        movement.qty = qty
        
        db.session.commit()
        flash('Product movement updated successfully!', 'success')
        return redirect(url_for('movements'))
    
    return render_template('add_edit_forms.html', type='movement', action='Edit', 
                          item=movement, products=products, locations=locations)

@app.route('/delete_movement/<movement_id>')
def delete_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    db.session.delete(movement)
    db.session.commit()
    flash('Product movement deleted successfully!', 'success')
    return redirect(url_for('movements'))

# Balance Report
@app.route('/balance')
def balance():
    # Calculate balance using SQL queries
    incoming = db.session.query(
        ProductMovement.product_id,
        ProductMovement.to_location.label('location_id'),
        func.sum(ProductMovement.qty).label('total_in')
    ).filter(ProductMovement.to_location.isnot(None)).group_by(
        ProductMovement.product_id, ProductMovement.to_location
    ).subquery()
    
    outgoing = db.session.query(
        ProductMovement.product_id,
        ProductMovement.from_location.label('location_id'),
        func.sum(ProductMovement.qty).label('total_out')
    ).filter(ProductMovement.from_location.isnot(None)).group_by(
        ProductMovement.product_id, ProductMovement.from_location
    ).subquery()
    
    balance_query = db.session.query(
        Product.product_id,
        Product.name.label('product_name'),
        Location.location_id,
        Location.name.label('location_name'),
        (func.coalesce(incoming.c.total_in, 0) - func.coalesce(outgoing.c.total_out, 0)).label('balance')
    ).select_from(Product).join(Location).outerjoin(
        incoming, (Product.product_id == incoming.c.product_id) & (Location.location_id == incoming.c.location_id)
    ).outerjoin(
        outgoing, (Product.product_id == outgoing.c.product_id) & (Location.location_id == outgoing.c.location_id)
    ).filter(
        (incoming.c.total_in.isnot(None)) | (outgoing.c.total_out.isnot(None))
    ).all()
    
    return render_template('balance.html', balance_data=balance_query)

if __name__ == '__main__':
    app.run(debug=True)