from flask import Flask, render_template, url_for, request, session, redirect, jsonify,flash
import pymongo
from datetime import timedelta, datetime
import numpy as np
import math
import requests
import json


# SETTING UP MOONGO ATLAS
client = pymongo.MongoClient("mongodb+srv://testuser:test@cluster0.8ondf.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.get_database('book_store')
books = db.books_db
cust = db.members
trans = db.transaction

app = Flask(__name__, static_url_path='/static')




# def displayPage(item_res,html_pg,)

def display_books():
    books_res =[x for x in  books.find({},{'bookID':1,'title':1, 'authors':1, 'isbn':1, 'publisher':1,'  num_pages':1,'stock':1 })]
    if len(books_res)==0:
        return render_template('books.html',books_res=books_res, mess=0)
    return render_template('books.html',books_res=books_res, mess=1)

def display_members():
    cust_res =[x for x in cust.find({})] 
    if len(cust_res)==0:
        return render_template('member.html',cust_res=cust_res, mess=0)
    return render_template('member.html',cust_res=cust_res, mess=1)

def display_transaction():
    trans_res =[x for x in trans.find({})]
    books_res =[x for x in books.find({},{'bookID':1,'title':1,'isbn':1,})]
    cust_res =[x for x in cust.find({},{'memID':1,'name':1})] 

    if len(trans_res)==0:
        return render_template('transaction.html',trans_res=trans_res,books_res=books_res,cust_res=cust_res, mess=0)
    return render_template('transaction.html',trans_res=trans_res,books_res=books_res,cust_res=cust_res, mess=1)



#Route for index
@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/books', methods=['POST','GET'])
def books_page():
    if request.method == "GET":
        return display_books()

@app.route('/member', methods=['POST','GET'])
def mem_page():
    if request.method == "GET":
        return display_members()

@app.route('/transaction', methods=['POST','GET'])
def transaction_page():
    if request.method == "GET":
        return display_transaction()
    
    

@app.route('/import_frappe', methods=['GET'])
def import_frappe():
    url = "https://frappe.io/api/method/frappe-library?page=9"
    imp_books = requests.get(url).json()['message']
    for bk in imp_books:
        if not books.find_one({'bookID':bk['bookID']}):
            books.insert_one(bk)        
    return display_books()

    
@app.route('/updatebook', methods=['GET','POST'])
def updatebook():
    pk = request.form['updtxtidOLD']
    books.update_one({"bookID":pk},{'$set':{'bookID':request.form['updtxtid'],
    'title':request.form['updtxttitle'],
    'author':request.form['updtxtauthor'],
    'isbn':request.form['updtxtisbn'],
    'publisher':request.form['updtxtpubl'],
    '  num_pages':request.form['updtxtpagenum'],
    'stock':request.form['updtxtstock']

    }})
    return redirect('/books')
     
@app.route('/addbook', methods=['GET', 'POST'])
def create_record():
    bk = {
        'bookID':request.form['txtid'],
    'title' : request.form['txttitle'],
    'authors' : request.form['txtauthor'],
    'isbn' : request.form['txtisbn'],
    'publisher' : request.form['txtpubl'],
    'num_page' : request.form['txtpagenum'],
    'stock':request.form['txtstock']}
    books.insert_one(bk)
    return redirect('/books')
 
@app.route('/delete/<string:getid>', methods = ['POST','GET'])
def delete_book(getid):
    book_ = books.find_one({'bookID':getid})
    if not book_:
        flash(f'Data not found!','danger')
        return redirect(url_for('books_page'))
    else:
        books.delete_one({'bookID':getid}) 
    return redirect('/books')




##############################    for members        #############

@app.route('/updatemember', methods=['POST'])
def updatemember():
    pk = request.form['updtxtmemIDOLD']
    books.update_one({"memID":pk},{'$set':{'memID':request.form['updtxtid'],
    'name':request.form['updtxtname'],
    'phone':request.form['updtxtphone'],
    'email':request.form['updtxtemail'],
    'fine':request.form['updtxtfine']
    }})
    
    return redirect('/member')
     
@app.route('/addmember', methods=['GET', 'POST'])
def create_member():
    mem = {
    'memID': request.form['txtmemID'],
    'name' : request.form['txtname'],
    'phone' : request.form['txtphone'],
    'email' : request.form['txtemail'],
    'fine' : 0}
    cust.insert_one(mem)
    return redirect('/member')
 
@app.route('/deletemem/<string:getid>', methods = ['POST','GET'])
def delete_mem(getid):
    if not cust.find_one({'memID':getid}):
        flash(f'Data not found!','danger')
        return redirect(url_for('mem_page'))
    cust.delete_one({'memID':getid}) 
    return redirect('/member')


##################### transaction     #############

@app.route('/addtrans', methods=['GET', 'POST'])
def create_trans():
    trans_type = request.form['transtype']
    tr = {
    'transID': request.form['txtid'],
    'title' : request.form['txttitle'],
    'rentstatus': trans_type,
    'member' : request.form['txtmember'],
    'date' : request.form['txtdate'],
    }
    fine = cust.find_one({'name':tr['member']})['fine']+100
    if books.find_one({'title':tr['title']})['stock']<=0:
        flash(f'selected book is out of stock!','danger')
        return redirect(url_for('transaction_page'))

    if trans_type == 'rent':
        if cust.find_one({'name':tr['member']})['fine']+100 >500:
            flash(f' {tr["member"]} has reached their Rental Debt Limit!','danger')
            return redirect(url_for('transaction_page'))
        tr['feestatus'] = "Unpaid"
        cust.update_one({'name':tr['member']},{'$set':{'fine':fine}})
        trans.insert_one(tr)
        return redirect(url_for('transaction_page'))
    
    if trans_type == 'return':
        tr['feestatus'] = "Paid"
        cust.update_one({'name':tr['member']},{'$set':{'fine':fine-200}})
        trans.insert_one(tr)
        return redirect(url_for('transaction_page'))

@app.route('/deletetrans/<string:getid>', methods = ['POST','GET'])
def delete_trans(getid):
    if not trans.find_one({'transID':getid}):
        flash(f'Data not found!','danger')
        return redirect(url_for('trans_page'))
    trans.delete_one({'transID':getid}) 
    return redirect('/transaction')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
 
