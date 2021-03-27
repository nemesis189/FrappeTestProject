from flask import Flask, render_template, url_for, request, session, redirect, jsonify,flash
import pymongo
from datetime import timedelta, datetime
import numpy as np
import math
import requests
import json
import dns


# SETTING UP MOONGO ATLAS
client = pymongo.MongoClient("mongodb+srv://testuser:test@cluster0.8ondf.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.get_database('book_store')
books = db.books_db
cust = db.members
trans = db.transaction

app = Flask(__name__, static_url_path='/static')


imp_books = []
for i in range (0,11):
    try:
        url = f"https://frappe.io/api/method/frappe-library?page={str(i)}"
        imp_books = imp_books + requests.get(url).json()['message']
    except:
        continue


def display_books():
    books_res =[x for x in  books.find({},{'bookID':1,'title':1, 'authors':1, 'isbn':1, 'publisher':1,'  num_pages':1,'stock':1 })]
    return render_template('books.html',books_res=books_res)

def display_members():
    cust_res =[x for x in cust.find({})] 
    return render_template('member.html',cust_res=cust_res)

def display_transaction():
    trans_res =[x for x in trans.find({})]
    books_res =[x for x in books.find({},{'bookID':1,'title':1,'isbn':1,})]
    cust_res =[x for x in cust.find({},{'memID':1,'name':1})] 
    return render_template('transaction.html',trans_res=trans_res,books_res=books_res,cust_res=cust_res)



#Route for index
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/books', methods=['GET','DELETE'])
def books_page():
    if request.method == 'DELETE':
        getid = request.get_data('id').decode('utf-8').split('=')[1]
        if not books.find_one({'bookID':getid}):
            flash('Data not found!','danger')
            return jsonify({'redirect': url_for("books_page")})
        books.delete_one({'bookID':getid})
        flash(f'Book record with ID:{getid} deleted successfully','success')
        return jsonify({'redirect': url_for("books_page")})
    
    if request.method == 'GET':
        return display_books()

@app.route('/member', methods=['GET','DELETE'])
def mem_page():
    if request.method == 'DELETE':
        getid = request.get_data('id').decode('utf-8').split('=')[1]
        if not cust.find_one({'memID':getid}):
            flash(f'Data not found!','danger')
            return jsonify({'redirect': url_for("mem_page")})
        cust.delete_one({'memID':getid})
        flash(f'Member record with ID:{getid} deleted successfully','success')
        return jsonify({'redirect': url_for("mem_page")})

    if request.method == 'GET':
        return display_members()


@app.route('/transaction', methods=['GET','DELETE'])
def transaction_page():
    if request.method == 'DELETE':
        getid = request.get_data('id').decode('utf-8').split('=')[1]
        if not trans.find_one({'transID':getid}):
            flash(f'Data not found!','danger')
            return jsonify({'redirect': url_for("transaction_page")})
        trans.delete_one({'transID':getid})
        flash(f'Transaction record with ID:{getid} deleted successfully','success')
        return jsonify({'redirect': url_for("transaction_page")})

    if request.method =='GET':
        return display_transaction()


@app.route('/books/import_frappe', methods=['GET'])
def import_frappe():  
    for bk in imp_books:
        if not books.find_one({'bookID': bk['bookID']}):
            books.insert_one(bk)
    flash(f'Data from Frappe API loaded successfully','success')
    return redirect('/books')


@app.route('/updatebook', methods=['POST'])
def updatebook():
    id = request.form['updtxtidOLD']
    new_val = {
        'bookID':       request.form['updtxtid'],
        'title':        request.form['updtxttitle'],
        'author':       request.form['updtxtauthor'],
        'isbn':         request.form['updtxtisbn'],
        'publisher':    request.form['updtxtpubl'],
        '  num_pages':  request.form['updtxtpagenum'],
        'stock':        request.form['updtxtstock']
        }
    books.update({"bookID":id},{'$set':new_val})
    return redirect('/books')

@app.route('/addbook', methods=['POST'])
def create_record():
    bk = {
        'bookID':          request.form['txtid'],
        'title' :          request.form['txttitle'],
        'authors' :        request.form['txtauthor'],
        'isbn' :           request.form['txtisbn'],
        'publisher' :      request.form['txtpubl'],
        '  num_pages' :    request.form['txtpagenum'],
        'stock':           request.form['txtstock']
        }
    books.insert_one(bk)
    return redirect('/books')

##############################    for members  #############

@app.route('/updatemember', methods=['POST'])
def updatemember():
    pk = request.form['updtxtmemIDOLD']
    cust.find_one_and_update({"memID":pk} , 
    {'$set':{'memID':request.form['updtxtmemID'],
    'name':request.form['updtxtname'],
    'phone':request.form['updtxtphone'],
    'email':request.form['updtxtemail'],
    'fine':request.form['updtxtfine']
    }})
    return redirect('/member')
     
@app.route('/addmember', methods=[ 'POST'])
def create_member():
    mem = {
    'memID': request.form['txtmemID'],
    'name' : request.form['txtname'],
    'phone' : request.form['txtphone'],
    'email' : request.form['txtemail'],
    'fine' : 0
    }
    if cust.find_one({'memID':mem['memID']}):
        flash(f'User with same Id exists. Please use a different id!','danger')
        return redirect(url_for('mem_page'))
    cust.insert_one(mem)
    return redirect('/member')


##################### transaction #############

@app.route('/addtrans', methods=[ 'POST'])
def create_trans():
    trans_type = request.form['transtype']
    tr = {
    'transID': request.form['txtid'],
    'title' : request.form['txttitle'],
    'rentstatus': trans_type,
    'member' : request.form['txtmember'],
    'date' : request.form['txtdate'],
    }
    if trans.find_one({'transID':tr['transID']}):
        flash(f'A transaction with same Id exists. Please use a different id!','danger')
        return redirect(url_for('mem_page'))

    fine = int(cust.find_one({'name':tr['member']})['fine'])+100
    if books.find_one({'title':tr['title']})['stock' ]<= 0:
        flash(f'selected book is out of stock!','danger')
        return redirect(url_for('transaction_page'))

    if trans_type == 'rent':
        if fine >500:
            flash(f' {tr["member"]} has reached their Rental Debt Limit!','danger')
            return redirect(url_for('transaction_page'))
        tr['feestatus'] = "Unpaid"
        cust.find_one_and_update( {'name': tr['member'] }, {'$set': {'fine':fine} })
        trans.insert_one(tr)
        return redirect(url_for('transaction_page'))
    
    if trans_type == 'return':
        tr['feestatus'] = "Paid"
        cust.find_one_and_update({'name': tr['member'] }, {'$set':  {'fine':fine-200} })
        trans.insert_one(tr)
        return redirect(url_for('transaction_page'))



if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
 
