from flask import Flask, render_template, url_for, request, session, redirect, jsonify,flash
import pymongo
from functools import wraps
from datetime import timedelta, datetime
from passlib.hash import pbkdf2_sha256
import uuid
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
app.secret_key = 'mysecret'


def start_session(user):
    # if user['_id']:
        # del user['_id']
    del user['password']          
    session['logged_in'] = True       
    session['user'] = user        #ASSIGNING CURRENT USER AS OBJ TO SESSION USER VARIABLE 
    return redirect(url_for('dash'))

#Method for verifying and logging in 
def login():
    user = cust.find_one({
        "email": request.form.get('email')
    },{'_id':0})
    if user and pbkdf2_sha256.verify(request.form.get('pass'), user['password']):
        return start_session(user)

    flash(f'Login Failed! Invalid credintials','danger') 
    return redirect(url_for('index'))


# Route for signing out, clearing session
@app.route('/signout')
def signout():
    session.clear()
    return redirect('/')

def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  return wrap    


@login_required
def display_books():
    books_res =[x for x in  books.find({},{'bookID':1,'title':1, 'authors':1, 'isbn':1, 'publisher':1,'  num_pages':1,'stock':1 })]
    return render_template('books.html',books_res=books_res)

@login_required
def display_members():
    cust_res =[x for x in cust.find({})] 
    return render_template('member.html',cust_res=cust_res)

@login_required
def display_transaction():
    if session['user']['admin']:
        trans_res =[x for x in trans.find({})]
    else:
        trans_res =[x for x in trans.find({'member':session['user']['name']})]
    books_res =[x for x in books.find({},{'bookID':1,'title':1,'isbn':1,})]
    cust_res =[x for x in cust.find({},{'memID':1,'name':1})] 
    return render_template('transaction.html',trans_res=trans_res,books_res=books_res,cust_res=cust_res)



##### All basic routes
@app.route('/',methods=['GET', 'POST'])
def index():
    if 'user' in session:
        return redirect('dash')
    if request.method == 'POST':
        return login()
    return render_template('index.html')

@app.route('/dash',methods=['GET'])
@login_required
def dash():
    return render_template('dash.html')



#Route for registering user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        user = {                                    #creating user object with user details
        "memID": str(uuid.uuid4().fields[-1])[:5],
        "name": request.form.get('reg_fname'),
        "phone": request.form.get('reg_phone'),
        "email": request.form.get('reg_email'),
        "password": request.form.get('reg_pass'),
        "admin":0,
        'fine':0
        }
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        axx = cust.find_one({ "email": user['email'] },{'_id':0})
        print(axx)

        if axx:
            ue = user['email']
            flash(f'Account already in use for { ue }!','danger') 
            return redirect('register')

        if cust.find_one({'memID':user['memID']},{'_id':0}):
            flash(f'User with same Id exists. Please use a different id!','danger')
            return redirect('register')

        if cust.insert_one(user):  
            #Inserting user info into database
            del user['_id']
            return start_session(user)

        flash(f'Signup failed !','danger') 
        return redirect('register')


    return render_template('register.html')         #rendering registration page if req == GET




@app.route('/books', methods=['GET','DELETE'])
def books_page():
    if request.method == 'DELETE':
        getid = request.get_data('id').decode('utf-8').split('=')[1]
        if not books.find_one({'bookID':getid},{'_id':0}):
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
        if not cust.find_one({'memID':getid},{'_id':0}):
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
        if not trans.find_one({'transID':getid},{'_id':0}):
            flash(f'Data not found!','danger')
            return jsonify({'redirect': url_for("transaction_page")})
        trans.delete_one({'transID':getid})
        flash(f'Transaction record with ID:{getid} deleted successfully','success')
        return jsonify({'redirect': url_for("transaction_page")})

    if request.method =='GET':

        return display_transaction()
        

@app.route('/reports',methods=['GET'])
def reports():
    if session['user']['admin']:
        list_of_trans = list(trans.find({}, {'_id':0,'title':1, 'member':1, 'date':1}))
        list_of_trans_rent = list(trans.find({'rentstatus':'rent'}, {'_id':0,'title':1, 'member':1, 'date':1}))
        titles = [ x['title'] for x in list_of_trans ]
        members = [ x['member'] for x in list_of_trans ]
        print(list_of_trans_rent)
    else:
        list_of_trans = list(trans.find({'member':session['user']['name']}, {'_id':0,'title':1, 'member':1, 'date':1}))
        list_of_trans_rent = list(trans.find({'member':session['user']['name'],'rentstatus':'rent'}, {'_id':0,'title':1, 'member':1, 'date':1}))
        titles = [ x['title'] for x in list_of_trans ]
        members = [ x['member'] for x in list_of_trans ]


    # print(list_of_trans, list_of_trans_rent)
    print(titles,members)
    title_count = { title: titles.count(title) for title in titles }
    member_count = { mem: members.count(mem) for mem in members }
    final_titles = sorted(title_count.items(), key = lambda kv:(kv[1], kv[0]), reverse = True )
    final_members = sorted(member_count.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)
    print(final_titles)
    
    return render_template('reports.html',list_of_trans_rent= list_of_trans_rent, final_members=final_members,final_titles=final_titles, title_count=title_count )


####### Routes for additional functions

@app.route('/books/import_frappe', methods=['GET'])
def import_frappe():
    imp_books = []
    for i in range (0,6):
        try:
            url = f"https://frappe.io/api/method/frappe-library?page={str(i)}"
            imp_books = imp_books + requests.get(url).json()['message']
        except:
            continue
    for bk in imp_books:
        if not books.find_one({'bookID': bk['bookID']},{'_id':0}):
            bk['stock'] = 50
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
    bid = str(uuid.uuid4().fields[-1])[:5]
    while books.find_one({'bookID':bid},{'_id':0}):
        bid = str(uuid.uuid4().fields[-1])[:5]

    bk = {
        'bookID':          bid,
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
    mid = str(uuid.uuid4().fields[-1])[:5]
    while books.find_one({'memID':mid},{'_id':0}):
        mid = str(uuid.uuid4().fields[-1])[:5]

    mem = {
    'memID': mid,
    'name' : request.form['txtname'],
    'phone' : request.form['txtphone'],
    'email' : request.form['txtemail'],
    'password':request.form['txtpass'],
    'fine' : 0
    }
    mem['password'] = pbkdf2_sha256.encrypt(mem['password'])
    axx = cust.find_one({ "email": mem['email'] },{'_id':0})

    if axx:
        ue = mem['email']
        flash(f'Account already in use for { ue }!','danger') 
        return redirect(url_for('mem_page'))

    if cust.find_one({'memID':mem['memID']},{'_id':0}):
        flash(f'User with same Id exists. Please use a different id!','danger')
        return redirect(url_for('mem_page'))

    if cust.insert_one(mem):  
        #Inserting mem info into database
        del mem['_id']
    if cust.find_one({'memID':mem['memID']},{'_id':0}):
        flash(f'User with same Id exists. Please use a different id!','danger')
        return redirect(url_for('mem_page'))
    cust.insert_one(mem)
    return redirect('/member')


##################### transaction #############

@app.route('/addtrans', methods=[ 'POST'])
def create_trans():
    tid = str(uuid.uuid4().fields[-1])[:5]
    while books.find_one({'memID':tid},{'_id':0}):
        tid = str(uuid.uuid4().fields[-1])[:5]
    trans_type = request.form['transtype']
    getdate = str(datetime.now().date()) if not session['user']['admin'] else request.form['txtdate']
    tr = {
    'transID': tid,
    'title' : request.form['txttitle'],
    'rentstatus': trans_type,
    'member' : request.form['txtmember'],
    'date' : getdate,
    'returndate':'Not Returned' ,
    }

    if trans.find_one({'transID':tr['transID']},{'_id':0}):
        flash(f'A transaction with same Id exists. Please use a different id!','danger')
        return redirect(url_for('transaction_page'))

    fine = int(cust.find_one( {'name': tr['member']},{'_id':0} )['fine']) 
    print(fine)
    new_stock = int(books.find_one( { 'title': tr['title']} ,{'_id':0})['stock'])

    if new_stock <= 0:
        flash(f'selected book is out of stock!','danger')
        return redirect(url_for('transaction_page'))

    if trans_type == 'rent':
        if fine >=500:
            flash(f' {tr["member"]} has reached their Rental Debt Limit!','danger')
            return redirect(url_for('transaction_page'))
        tr['feestatus'] = "Unpaid"
        cust.find_one_and_update( {'name': tr['member'] }, {'$set': {'fine':fine+100} })
        books.find_one_and_update( { 'title': tr['title']}, {'$set': { 'stock': new_stock-1 }} )
        trans.insert_one(tr)
        return redirect(url_for('transaction_page'))
    
    if trans_type == 'return':
        tid=request.form['txtid']
        cust.find_one_and_update({'name': tr['member'] }, {'$set':  {'fine':fine-100} })
        print(cust.find_one({'name': tr['member'] }))
        books.find_one_and_update( { 'title': tr['title']}, {'$set': { 'stock': new_stock+1 }} )
        print(books.find_one({'title': tr['title'] }))

        trans.find_one_and_update({'transID': tid},{'$set':{'feestatus':"Paid",'rentstatus':'Returned','returndate':str(datetime.now().date())}})
        print(trans.find_one({'transID': tid }))

        return redirect(url_for('transaction_page'))


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'mysecret'
    app.run(debug=True)

