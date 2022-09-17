from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import Items
from flask_login import login_required,current_user
from core_market_data.forms import PurchaseItemForm,SellItemForm
from . import db
views=Blueprint('views',__name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html')

@views.route('/market',methods=['GET','POST'])
@login_required
def market_page():
    #purchase logic
    purchase_form=PurchaseItemForm()
    sell_form=SellItemForm()
    if request.method=='POST':
        Purchased_item=request.form.get('Purchased_item')
        p_item_object=Items.query.filter_by(name=Purchased_item).first()
        if p_item_object:
            if current_user.budget<p_item_object.price:
                flash(f"Your budget not sufficient to purchase the item {Purchased_item}",category='error')
            else:
                p_item_object.owner=current_user.id
                current_user.budget -= p_item_object.price
                db.session.commit()
                flash(f"Congratulation You Purchased the item {Purchased_item}")

        #sell logic
        sold_item=request.form.get('sell_item')
        s_item_object = Items.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulation you sold the item {sold_item} back to market", category='error')
            else:
                flash('Something want wrong in selling the item', category='error')

        return redirect(url_for('views.market_page'))
        #if purchase_form.validate_on_submit():
        #    print(request.form.get('Purchased_item'))
    if request.method=="GET":
        items=Items.query.filter_by(owner=None)
        owned_items=Items.query.filter_by(owner=current_user.id)
        return render_template('market.html',items=items,purchase_form=purchase_form,owned_items=owned_items,sell_form=sell_form)


