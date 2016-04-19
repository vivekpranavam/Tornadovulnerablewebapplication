import tornado.ioloop
import tornado.web
import cgi
import sqlite3
import tornado.template
import os
import sqlite3 as lite

def CreateDB():
    con = lite.connect('db.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'user'")
        x=cur.fetchone()[0]
        print x

        if x==0:
            cur.execute("CREATE TABLE user(userid varchar(10),username varchar(20), password varchar(20),age integer)")
            con.commit()        
        return x    

#Xss part
class LoginXss(tornado.web.RequestHandler):
        def get(self):
                return self.render('login.html')
class HomeHandler(tornado.web.RequestHandler):

        def post(self):
                username=self.get_argument("name")
                password=self.get_argument("password")                
                con = lite.connect('db.db')
                with con:
                    cur = con.cursor()
                    cur.execute("SELECT count(*) FROM user WHERE username= %s and password= %s" %("'"+username+"'","'"+password+"'"))
                    x=cur.fetchone()[0]
                    if x!=0:
                        self.write('<html><body bgcolor="#E6E6FA"><p>Welcome ' + username + '</p>'
                                    '<a href="/userlist">List All The Users</a><br><br>'
                                    '<a href="/dom">DOMXSS Example</a><br><br>'
                                    '<a href="/SQLiload">SQLi Example</a><br><br>'                                
                                    '<a href="/login">Logout</a></body></html>')
                    else:
                        self.write('<html><body><script>alert("Invalid Useraname or Password..!")</script>'
                                   '<a href="/login">BackToLogin</a></body></html>')               
                

class SignupXss(tornado.web.RequestHandler):
        def get(self):
                return self.render("usersignup.html")  
        
        def post(self):                              
                username=self.get_argument("fname")
                userid=self.get_argument("userid")
                password=self.get_argument("password")
                age=self.get_argument("age")               
                con = lite.connect('db.db')
                with con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO user VALUES(?,?,?,?)",(userid,username,password,age))
                    self.write('<html><body><script>alert("UserRegistration sucess..!")</script>'
                                '<a href="/login">BackToLogin</a></body></html>')
class DOMXss(tornado.web.RequestHandler):
        def get(self):
                return self.render("dom.html")


class ListuserXss(tornado.web.RequestHandler):
        def get(self):
            con = lite.connect('db.db')
            with con:
                cur = con.cursor()
                x=cur.execute("select username,password from user")        
                
                for l1 in x:
                    self.write(l1[0])
                    self.write(l1[1])
                    print "ID = ", l1[1]
class SQLiLoadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("usercd.html")

class SQLiHandler(tornado.web.RequestHandler):   
    def get(self):        
        userid=self.get_argument("uid")
        #self.write(userid)        
        con=lite.connect('db.db')
        with con:
            cur=con.cursor()           
            x=cur.execute("select userid,username from user where userid=%s" %("'"+userid+"'"))
            self.write('<html><body><table style="width:50%"> <tr> <td>USERID</td><td>USERNAME</td></tr>'
                        '</table></body></html>')
            for l1 in x:
                print l1[0]
                print l1[1]
                self.write('<html><body><table style="width:50%"><tr> <td>' + l1[0] + '</td><td>' + l1[1] + '</td></tr>'
                            '</table>'
                            '</body></html>')
                
                         
    
                             
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
settings = {
            "debug": True,
            "template_path": os.path.join(BASE_DIR, "templates"),
            "static_path": os.path.join(BASE_DIR, "static")
        }  

                        
                        
def make_app():
        return tornado.web.Application([(r"/login", LoginXss),(r"/home", HomeHandler),(r"/user",SignupXss),
            (r"/userlist",ListuserXss),(r"/SQLiload",SQLiLoadHandler),(r"/userdetails",SQLiHandler),(r"/dom",DOMXss)],**settings)
        
if __name__ == "__main__":
    CreateDB()
    app = make_app()
    app.listen(7777)               
    tornado.ioloop.IOLoop.current().start()
