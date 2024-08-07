from flask import Flask, render_template, url_for, current_app, g, request, redirect, flash
from email_validator import validate_email, EmailNotValidError


app = Flask(__name__) 
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"

@app.route("/")
def index():
    return "Hellow, flask"

@app.route("/hello/<name>",
           methods=["GET"],
           endpoint="hello-endpoint"
           )
def hello(name):
    #python3.6から導入されたf-stringで文字列を定義
    return f"Hello world,{name}!!!!!"

@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)

with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello-endpoint", name="world"))
    print(url_for("show_name", name="muto", page="1"))

ctx = app.app_context()
ctx.push()

print(current_app.name)

g.connection = "connection"
print(g.connection)

with app.test_request_context("/users?updated=true"):
    print(request.args.get("updated"))


#問い合わせフォーム
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        #form属性を使ってフォームの値を取得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]
        #入力チェック
        is_valid = True

        if not username:
            flash("ユーザー名は必須です")
            is_valid = False
        
        if not email:
            flash("メールアドレスは必須です")
            is_valid = False
        
        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False
        
        if not description:
            flash("お問い合わせは必須です")
            is_valid = False
        
        if not is_valid:
            return redirect(url_for("contact"))
        #メールを送る

        #contactエンドポイントにリダイレクトする
        flash("お問い合わせありがとうございました")
        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")



if __name__ == "__main__":
    app.run(debug=True)