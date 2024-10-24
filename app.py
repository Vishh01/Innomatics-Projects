from flask import Flask, request, render_template
import re

app = Flask(__name__)

##################################
@app.route('/')
def index():
    return render_template("home.html")


@app.route("/find_match", methods=['POST'])
def find_match():
        patt = re.compile(str(request.form['patt']))
        string = str(request.form['str'])
        
        matches = re.finditer(patt, string)
        
        match_list = [i.group() for i in matches]
        
        number = len(match_list)
        not_found = True if len(match_list)==0 else False        
        return render_template("checker.html",match_list = match_list, not_found = not_found,number = number)


@app.route("/email",methods = ["POST"])
def email():
    return render_template("email.html")

@app.route("/validate",methods = ["POST"])
def validate():
    email_patt = "^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    mail_val = str(request.form['email_val'])
    
    valid = re.match(email_patt, mail_val)
    
    result = mail_val + " is a valid e-mail ID." if valid else mail_val + "is not a valid e-mail ID."
    return render_template("email.html",valid = valid,result = result)




##################################

if __name__ == "__main__":
    app.run(debug=True,)
    
    
    
    

