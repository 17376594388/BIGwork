# -*- coding: utf-8-*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('./functions/')
from flask import Flask,render_template,request,redirect, url_for, flash, session,json,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import hashlib
import mail
import proof
import exceptions

conn = sqlite3.connect('data.db',check_same_thread=False)
cursor = conn.cursor()
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#函数定义
def current_user():
    if session['ID'] and session['username']:
        return True
    else:
        return False
def login_vaild(user_name,user_pwd):
    cursor.execute('select * from users where username="'+user_name+'" and userpwd="'+user_pwd+'"')
    result = cursor.fetchall()
    if result:
        session['ID'] = result[0][0]
        session['username']=result[0][1].encode("utf-8")
        return True
    else:
        return False
def sign_isexist(user_name):
    cursor.execute('select * from users where username="'+user_name+'"')
    result = cursor.fetchall()
    if result:
        raise Exception("304")
def find_notexist(user_name):
    cursor.execute('select * from users where username="'+user_name+'"')
    result = cursor.fetchall()
    if not result:
        raise Exception("305")
def insertuser(user_name,user_pwd):
    try:
        user_pwd=hashlib.md5(user_pwd).hexdigest()
        cursor.execute('INSERT INTO users VALUES (NULL, "'+user_name+'", "'+user_pwd+'")')
        conn.commit()
    except:
        conn.rollback()
def updateuser(user_name,user_pwd):
    try:
        user_pwd=hashlib.md5(user_pwd).hexdigest()
        cursor.execute('UPDATE users SET userpwd="'+user_pwd+'" where username="'+user_name+'"')
        conn.commit()
    except:
        conn.rollback()          
def findID(user_name):
    cursor.execute('select ID from users where username="'+user_name+'"')
    result=cursor.fetchall()
    return result[0][0]
def findpwd(user_name):
    cursor.execute('select userpwd from users where username="'+user_name+'"')
    result=cursor.fetchall()
    return result[0][0]
def get_option_sub(userid):
    lst=[]
    cursor.execute('select count(*) from records where userid='+str(userid)+' and subid <=1000')
    lst.append(cursor.fetchall()[0][0])
    cursor.execute('select count(*) from option_sub ')
    lst.append(cursor.fetchall()[0][0]-lst[0])
    return lst
def get_multioption_sub(userid):
    lst=[]
    cursor.execute('select count(*) from records where userid='+str(userid)+' and subid >2000')
    lst.append(cursor.fetchall()[0][0])
    cursor.execute('select count(*) from multioption_sub ')
    lst.append(cursor.fetchall()[0][0]-lst[0])
    return lst
def get_fill_sub(userid):
    lst=[]
    cursor.execute('select count(*) from records where userid='+str(userid)+' and subid >1000 and subid<=2000')
    lst.append(cursor.fetchall()[0][0])
    cursor.execute('select count(*) from fill_sub ')
    lst.append(cursor.fetchall()[0][0]-lst[0])
    return lst
def get_all_sub(userid):
    lst=[]
    s=0
    cursor.execute('select count(*) from records where userid='+str(userid)+'')
    lst.append(cursor.fetchall()[0][0])
    cursor.execute('select count(*) from option_sub ')
    s+=cursor.fetchall()[0][0]
    cursor.execute('select count(*) from fill_sub ')
    s+=cursor.fetchall()[0][0]
    cursor.execute('select count(*) from multioption_sub ')
    s+=cursor.fetchall()[0][0]
    lst.append(s-lst[0])
    return lst
def get_finish_subs(userid):
    lst=[]
    cursor.execute('select count(*) from records where userid='+str(userid)+' and subid <=1000')
    lst.append(cursor.fetchall()[0][0])
    cursor.execute('select count(*) from records where userid='+str(userid)+' and subid >1000 and subid<=2000')
    lst.append(cursor.fetchall()[0][0])
    cursor.execute('select count(*) from records where userid='+str(userid)+' and subid >2000')
    lst.append(cursor.fetchall()[0][0])
    return lst
def getsubcount(subtype):
    cursor.execute('select count(*) from '+str(subtype)+'')
    count=cursor.fetchall()[0][0]
    lst=[ i+1 for i in range(count)]
    return lst
def getdonesubid(subtype,userid):
    lst=[]
    if subtype=='option_sub':
        cursor.execute('select * from records where userid='+str(userid)+' and subid <=1000')
    elif subtype=='multioption_sub':
        cursor.execute('select * from records where userid='+str(userid)+' and subid >2000')
    elif subtype=='fill_sub':
        cursor.execute('select * from records where userid='+str(userid)+' and subid >1000 and subid<=2000')
    data=cursor.fetchall()
    for i in data:
        lst.append(i[1])
    return lst
def getoldans(subid,userid):
    lst=[]
    cursor.execute('select useran from records where userid='+str(userid)+' and subid='+str(subid)+'')
    result=cursor.fetchall()
    if result:
        if subid<=1000:
            lst.append(result[0][0])
        elif subid>1000 and subid<=2000:
            lst.append(result[0][0].encode("utf-8"))
        else:
            for i in result[0][0]:
                lst.append(i)
        return lst
    else:
        return []
def get_option_subject(sub_id):
    dic=dict()
    cursor.execute('select * from option_sub where ID='+str(sub_id)+'')
    data=cursor.fetchall()
    dic['ID']=data[0][0]
    dic['text']=data[0][1].encode("utf-8")
    dic['ansA']=data[0][2].encode("utf-8")
    dic['ansB']=data[0][3].encode("utf-8")
    dic['ansC']=data[0][4].encode("utf-8")
    dic['ansD']=data[0][5].encode("utf-8")
    dic['ans']=data[0][6]
    dic['reason']=data[0][7]
    session['answer']=data[0][6]
    session['subid']=data[0][0]
    return dic
def save_to_record(userid,subid,ans):
    cursor.execute('select * from records where userid='+str(userid)+' and subid='+str(subid)+'')
    result=cursor.fetchall()
    if result:
        try:
            cursor.execute('UPDATE records SET useran="'+ans+'" where userid='+str(userid)+' and subid='+str(subid)+'')
            conn.commit()
        except:
            conn.rollback()
    else:
        try:
            cursor.execute('INSERT INTO records VALUES ('+str(userid)+','+str(subid)+', "'+ans+'")')
            conn.commit()
        except:
            conn.rollback()
def collect_sub(userid,subid):
    cursor.execute('select * from collections where userid='+str(userid)+' and subid='+str(subid)+'')
    result=cursor.fetchall()
    if result:
        return '310'
    else:
        try:
            cursor.execute('INSERT INTO collections VALUES ('+str(userid)+','+str(subid)+')')
            conn.commit()
            return "210"
        except:
            conn.rollback()
def get_fill_subject(sub_id):
    dic=dict()
    cursor.execute('select * from fill_sub where ID='+str(sub_id)+'')
    data=cursor.fetchall()
    dic['ID']=data[0][0]
    dic['text']=data[0][1].encode("utf-8")
    dic['ans']=data[0][2].encode("utf-8")
    dic['reason']=data[0][3]
    session['answer']=data[0][2].encode("utf-8")
    session['subid']=data[0][0]
    return dic
def get_multioption_subject(sub_id):
    dic=dict()
    cursor.execute('select * from multioption_sub where ID='+str(sub_id)+'')
    data=cursor.fetchall()
    dic['ID']=data[0][0]
    dic['text']=data[0][1].encode("utf-8")
    dic['ansA']=data[0][2].encode("utf-8")
    dic['ansB']=data[0][3].encode("utf-8")
    dic['ansC']=data[0][4].encode("utf-8")
    dic['ansD']=data[0][5].encode("utf-8")
    dic['ansE']=data[0][6].encode("utf-8")
    dic['ans']=data[0][7]
    dic['reason']=data[0][8]
    session['answer']=data[0][7]
    session['subid']=data[0][0]
    return dic
def getsubid(userid):
    lst=[]
    cursor.execute('select subid from collections where userid='+str(userid))
    result=cursor.fetchall()
    lst=[row[0] for row in result]
    return lst
def getsubidcount(userid):
    cursor.execute('select subid from collections where userid='+str(userid))
    result=cursor.fetchall()
    lenth=len(result)
    return lenth
def getCollect_subject(subid_list):
    dic=dict()
    cursor.execute('select ID,subject from fill_sub')
    result=cursor.fetchall()
    for row in result:
        if row[0] in subid_list:
            dic[row[0]]=row[1].encode("utf-8")
    cursor.execute('select ID,subject from multioption_sub')
    result=cursor.fetchall()
    for row in result:
        if row[0] in subid_list:
            dic[row[0]]=row[1].encode("utf-8")
    cursor.execute('select ID,subject from option_sub')

    result=cursor.fetchall()
    for row in result:
        if row[0] in subid_list:
            dic[row[0]]=row[1].encode("utf-8")
    return dic
def get_useran(userid,sub_id):
    cursor.execute('select useran from records where userid='+str(userid)+' and subid='+str(sub_id)+'')
    result=cursor.fetchone()
    if(result==None):
        return "未做过"
    else:
        return result[0].encode("utf-8")
def get_subject(content,subid_list):
    dic=dict()
    cursor.execute('select ID,subject from multioption_sub where subject like \'%'+content+'%\'')
    result=cursor.fetchall()
    for row in result:
        if row[0] in subid_list:
            dic[row[0]]=row[1].encode("utf-8")
    cursor.execute('select ID,subject from fill_sub where subject like \'%'+content+'%\'')
    result=cursor.fetchall()
    for row in result:
        if row[0] in subid_list:
            dic[row[0]]=row[1].encode("utf-8")
    cursor.execute('select ID,subject from option_sub where subject like \'%'+content+'%\'')
    result=cursor.fetchall()
    for row in result:
        if row[0] in subid_list:
            dic[row[0]]=row[1].encode("utf-8")
    return dic
def getsub(subid):
    dic=dict()
    if(subid<1000):
        cursor.execute('select ID,subject from option_sub where ID='+str(subid)+'')
    elif(subid<2000):
        cursor.execute('select ID,subject from fill_sub where ID='+str(subid)+'')
    else:
        cursor.execute('select ID,subject from multioption_sub where ID='+str(subid)+'')
    result=cursor.fetchone()
    dic[result[0]]=result[1].encode("utf-8")
    return dic
def deleteidsub(sub_id,userid):
    try:
        cursor.execute('delete from collections where subid='+str(sub_id)+' and userid='+str(userid)+'')
        conn.commit()
        return "210"
    except:
        conn.rollback()
#路由
#登录验证
@app.route('/', methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        flag=login_vaild(request.form['username'].encode("utf-8"),hashlib.md5(request.form['userpwd'].encode("utf-8")).hexdigest())
        if flag==True:
            return "200"
        elif not request.form['username'] or not request.form['userpwd']:
            return '307'
        else:
            return '300'
    return render_template('login.html')
#注册
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        try:
            proof.checknull(request.form['userpwd'].encode("utf-8"))
            proof.checkemail(request.form['username'].encode("utf-8"),session['email'])
            proof.checknumber(request.form['checknum'].encode("utf-8"),session['checkcode'])
            proof.checkpwd(request.form['userpwd'].encode("utf-8"),request.form['userpwdagain'].encode("utf-8"))
            sign_isexist(request.form['username'].encode("utf-8"))
        except Exception as e:
            return str(e)
        else:
            insertuser(request.form['username'].encode("utf-8"),request.form['userpwd'].encode("utf-8"))
            session['username']=request.form['username'].encode("utf-8")
            session['ID']=findID(request.form['username'])
            return "200"

    return render_template('signup.html')
#找回密码
@app.route('/findback',methods=['GET','POST'])
def findback():
    if request.method=="POST":
        try:
            proof.checknull(request.form['newpwd'].encode("utf-8"))
            proof.checkemail(request.form['username'].encode("utf-8"),session['email'])
            proof.checknumber(request.form['checknum'].encode("utf-8"),session['checkcode'])
            proof.checkpwd(request.form['newpwd'].encode("utf-8"),request.form['newpwdagain'].encode("utf-8"))
            find_notexist(request.form['username'].encode("utf-8"))
        except Exception as e:
            return str(e)
        else:
            updateuser(request.form['username'].encode("utf-8"),request.form['newpwd'].encode("utf-8"))
            return '202'

    return render_template('findback.html')
#退出
@app.route('/out')
def out():
    session.clear()
    return redirect(url_for('login'))
#发邮箱验证码
@app.route('/sendMail',methods=['GET','POST'])
def sendMail():
    if request.method=='POST':
        val=mail.sendmail(request.form['address'])
        if val!='failed':
            session['checkcode']=val
            session['email']=request.form['address']
            print(val,session['checkcode'])
            return '201'
        else:
            return '306'

#首页
@app.route('/index',methods=['GET','POST'])
def index():
    if request.method=="POST":
        data=[]
        data.append(get_option_sub(session['ID']))
        data.append(get_fill_sub(session['ID']))
        data.append(get_multioption_sub(session['ID']))
        data.append(get_all_sub(session['ID']))
        data.append(get_finish_subs(session['ID']))
        return json.dumps(data)
    if current_user():
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
#选择题
@app.route('/option_sub/<int:sub_id>',methods=['GET','POST'])
def option_sub(sub_id):
    if request.method=='POST':
        save_to_record(session['ID'],sub_id,request.form['answer'])
        if session['answer']==request.form['answer']:
            return '1'
        else:
            return "-1"
    counts=getsubcount("option_sub")
    subject=get_option_subject(sub_id)
    donesubid=getdonesubid("option_sub",session['ID'])
    oldans=getoldans(sub_id,session['ID'])
    if current_user():
        return render_template('optionsub.html',counts=counts,subject=subject,donesubid=donesubid,oldans=oldans)
    else:
        return redirect(url_for('login'))
#填空题
@app.route('/fill_sub/<int:sub_id>',methods=['GET','POST'])
def fill_sub(sub_id):
    if request.method=='POST':
        save_to_record(session['ID'],sub_id,request.form['answer'])
        if session['answer']==request.form['answer']:
            return '1'
        else:
            return "-1"
    counts=getsubcount("fill_sub")
    subject=get_fill_subject(sub_id)
    donesubid=getdonesubid("fill_sub",session['ID'])
    oldans=getoldans(sub_id,session['ID'])
    if current_user():
        return render_template('fillsub.html',counts=counts,subject=subject,donesubid=donesubid,oldans=oldans)
    else:
        return redirect(url_for('login'))
#多选题
@app.route('/multioption_sub/<int:sub_id>',methods=['GET','POST'])
def multioption_sub(sub_id):
    if request.method=='POST':
        save_to_record(session['ID'],sub_id,request.form['answer'])
        if session['answer']==request.form['answer']:
            return '1'
        else:
            return "-1"
    counts=getsubcount("multioption_sub")
    subject=get_multioption_subject(sub_id)
    donesubid=getdonesubid("multioption_sub",session['ID'])
    oldans=getoldans(sub_id,session['ID'])
    if current_user():
        return render_template('multioptionsub.html',counts=counts,subject=subject,donesubid=donesubid,oldans=oldans)
    else:
        return redirect(url_for('login'))
#收藏题目
@app.route('/collect',methods=['GET','POST'])
def collect():
    if request.method=='POST':
        flag=collect_sub(session['ID'],session['subid'])
        return flag
#查找题目
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        subid = request.form.get('subid').encode("utf-8")
        subcontent = request.form.get('subcontent').encode("utf-8")
        if( subcontent!=''):
            subid_list1=getsubid(session['ID'])
            subject=get_subject(subcontent,subid_list1)
            counts=len(subject)
            subid_list=list(subject.keys())
            return render_template('collect_list.html',subject=subject,subid_list=subid_list)
        elif(subid!='' and subcontent==''):
            subid_list1=getsubid(session['ID'])
            if(int(subid) not in subid_list1):
                return render_template('collect_list.html')
            else:
                subject=getsub(int(subid))
                return render_template('collect_list.html',subject=subject,subid_list=[int(subid)])
        else:
            counts=getsubidcount(session['ID'])
            subid_list=getsubid(session['ID'])
            subject=getCollect_subject(subid_list)
            subid_list=subid_list[::-1]
            return render_template('collect_list.html',subject=subject,subid_list=subid_list)
    return redirect(url_for('collect_list'))
#删除收藏题目
@app.route('/deletesub',methods=['GET','POST'])
def deletesub():
    if request.method=='POST':
        id=int(request.form['id'].encode("utf-8"))
        flag=deleteidsub(id,session['ID'])
        return flag
#收藏列表
@app.route('/collect_list',methods=['GET','POST'])
def collect_list():
    if request.method=='POST':
        id=int(request.form['subid'].encode("utf-8"))
        if(id<1000):
            subject=get_option_subject(id)
        elif(id<2000):
            subject=get_fill_subject(id)
        else:
            subject=get_multioption_subject(id)
        useran=get_useran(session['ID'],id)
        subject['useran']=useran
        return subject
    counts=getsubidcount(session['ID'])
    subid_list=getsubid(session['ID'])
    subject=getCollect_subject(subid_list)
    subid_list=subid_list[::-1]
    if current_user():
        return render_template('collect_list.html',subject=subject,subid_list=subid_list)
    else:
        return redirect(url_for('login'))


