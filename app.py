
from flask import Flask , render_template, request, session, redirect, url_for,flash
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from flask_sqlalchemy import sqlalchemy
from wtforms import StringField, PasswordField, BooleanField, SubmitField,DateField
from wtforms.validators import DataRequired, Length, Email
from flask_login import UserMixin


from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,validators,Form,
                    RadioField, SelectField, TextField, TextAreaField,PasswordField,
                    SubmitField)
from wtforms.validators import DataRequired
from flask_login import LoginManager
from flask_login import login_manager
from flask_login import login_required
from flask import Blueprint
login_manager = LoginManager()
login_manager.login_view = 'footer'
auth = Blueprint('auth', __name__)
app =Flask (__name__)
def create_app(config_name):
    app =Flask (__name__)
    app.register_blueprint(auth, url_prefix='/auth')
    login_manager.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/collectedefondaide'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

    #c'est la cles secret insertion
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

app.config['SECRET_KEY'] = '3&91i)&lkxl@$et^leyvn8)tqa+4%7p5gg5gbrfj@(#kwhk5qs'
#pour envoyer les message de flask
public_key = "pk_test_TYooMQauvdEDq54NiTphI7jx"
db = SQLAlchemy(app)
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column( nullable=True)
    prenom = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=True)
    adresse = db.Column(db.String(80), nullable=False)
    telephone = db.Column(db.String(15), nullable=True)
    nomassociation = db.Column(db.String(80), nullable=True)
    cas = db.relationship('Cas', backref='user')
    def __repr__(self):
        return '<User %r>' % self.nom

class Cas(db.Model):
    __tablename__ = 'cas'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(), unique=True, index=True)
    montant = db.Column(db.Numeric(10,2), nullable=False)
    datelimite = db.Column(db.Date(), nullable=False)
    photo =db.Column(db.String(255),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    detaillecas = db.relationship('DetailleCas', backref='cas')
    dons = db.relationship('Dons', backref='cas')

    def __repr__(self):
        return '<Cas %r>' % self.description

class DetailleCas(db.Model):
    __tablename__ = 'detaillecas'
    id = db.Column(db.Integer, primary_key=True)
    sommecollecter = db.Column(db.Numeric(10,2), nullable=False)
    sommerestante = db.Column(db.Numeric(10,2), nullable=False)
    nombreDonnateur = db.Column(db.Numeric(10,2), nullable=False)
    cas_id = db.Column(db.Integer, db.ForeignKey('cas.id'))
    def __repr__(self):
        return '<DetailleCas %r>' % self.sommecollecter

class Dons(db.Model):
    __tablename__ = 'dons'
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.Text(), unique=True, index=True)
    montant = db.Column(db.Numeric(10,2), nullable=False)
    mode = db.Column(db.String(30), nullable=False)
    donnateur_id = db.Column(db.Integer, db.ForeignKey('donnateur.id'))
    cas_id = db.Column(db.Integer, db.ForeignKey('cas.id'))
    def __repr__(self):
        return '<Dons %r>' % self.commentaire   

class Donnateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(15), nullable=True)
    don = db.relationship('Dons', backref='donnateur')
    def __repr__(self):
        return '<Donnateur %r>' % self.nom


#les formulaire
class UserForm(Form):
    nom = StringField('Nom')
    prenom = StringField('Prenom')
    email = StringField('Email ', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('Mot de passe',  [validators.Length(min=8, max=35)])
    confirm = PasswordField('Repeat Password')
    adresse = StringField('Adresse', [validators.Length(min=4, max=25)])
    telephone = StringField('Telephone', [validators.Length(min=4, max=25)])
    nomassociation = StringField('Nom Association')
    cas = StringField('Cas')
    submit = SubmitField('Enregistrer')
    delete = SubmitField('Supprimer')
    modifier = SubmitField('Modifier')
class DonnateurForm(Form):
    nom = StringField('Nom', [validators.Length(min=4, max=25)])
    prenom = StringField('Prenom', [validators.Length(min=4, max=25)])
    email = StringField('Email ', [validators.Length(min=6, max=35),validators.Email()])
    telephone = StringField('Telephone', [validators.Length(min=9, max=15)])
    don = StringField('Dons')
    submit = SubmitField('Enregistrer')
    delete = SubmitField('Supprimer')
    modifier = SubmitField('Modifier')
class DonForm(Form):
    commentaire = StringField('Nom', [validators.Length(min=10, max=255)])
    montant = StringField('Montant')
    mode = SelectField('Mode de Payement', choices=[('Orange Money', 'Orange Money'), ('Wari', 'Wari')])
    donnnateur = StringField('Donnateur')
    cas = StringField('Cas')
    submit = SubmitField('Enregistrer')
    delete = SubmitField('Supprimer')
    modifier = SubmitField('Modifier')
class CasForm(Form):
    description = TextAreaField('Description', [validators.Length(min=10, max=255)])
    montant = StringField('Montant', [validators.Length(min=4, max=25)])
    datelimite =DateField('Date Limite', [validators.DataRequired()], format='%d/%m/%Y')
    photo = StringField('Photo',[validators.Length(min=10, max=255)])
    user = StringField('Utilisateur')
    don = StringField('Dons')
    #submit = SubmitField('Enregistrer')
   
class DetailleCasForm(Form):
    sommeCollecter = StringField('Somme Collecter')
    sommerestant = StringField('Somme Restant')
    nomrededonnateur = StringField('Nombre de Donnateur')
    cas = StringField('Cas')
    submit = SubmitField('Enregistrer')
    delete = SubmitField('Supprimer')
    modifier = SubmitField('Modifier')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
    Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    #submit = SubmitField('Se connecter')
app = Flask(__name__)
app.secret_key = "super secret key"
@app.route('/',methods=['GET', 'POST'])
def home():
    forme=LoginForm(request.form)
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
      
       try:
           
            #hash_password = bcrypt.generate_password_hash(form.password.data)
            user = User(nom=form.nom.data, prenom=form.prenom.data, email=form.email.data, adresse=form.adresse.data, password=form.password.data, telephone=form.telephone.data,nomassociation=form.nomassociation.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Merci {form.prenom.data} {form.nom.data} {form.nomassociation.data} pour se geste trés nomble de ta part veuiller se connecter avec votre compte {form.email.data}','success')
            return redirect(url_for('home',form=form,title="S'enregistrer",forme=forme))
       except sqlalchemy.exc.IntegrityError:
            flash(f'Merci  {form.prenom.data} {form.nom.data} {form.nomassociation.data}  pour se geste trés nomble de ta part veuiller se connecter avec votre compte {form.email.data}','danger')
    return render_template('footer.html',form=form,forme=forme)

@app.route('/cas',methods=['GET', 'POST'])
def cas():
    forme=CasForm(request.form)
    data = dict()
    data['id'] = session.get('id')
    data['nom'] = session.get('nom')
    data['prenom'] = session.get('prenom')
    data['nomassociation'] = session.get('nomassociation')
    if request.form.get('nouveau') is not None:
        cas = Cas()
        detail = DetailleCas()
        cas.description = forme.description.data
        cas.montant =forme.montant.data
        cas.photo = forme.photo.data
        cas.datelimite = forme.datelimite.data
        cas.user_id = session.get('id')
        db.session.add(cas)
        db.session.commit()
        detail.sommecollecter=0
        detail.sommerestante=0
        detail.cas_id=cas.id
        db.session.add(detail)
        db.session.commit()
        return redirect(url_for("listecas"))
    #cas = cas.query.filter_by(user_id=data['id']).all()    
    return render_template('cas.html',data=data,form=forme)



@app.route('/formtest')
def formtest():
    return render_template('formtest.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    forme=UserForm(request.form)
    user = User.query.filter_by(email=forme.email.data, password=forme.password.data).first()
    # return user.nom
    if user is None:
        return redirect(url_for("home"))
    else:
        # return user.nom
        session['nom'] = user.nom
        session['prenom'] = user.prenom
        session['nomassociation'] = user.nomassociation
        session['id'] = user.id
        return redirect(url_for("cas",data=session))
@app.route('/addcas', methods=['GET', 'POST'])
def addcas():
    form=CasForm(request.form)
    cas = Cas(description=form.description.data, montant=form.montant.data, photo=form.photo.data, datelimite=form.datelimite.data)
    db.session.add(cas)
    db.session.commit()
    #flash(f'Merci {form.prenom.data} {form.nom.data} pour se geste trés nomble de ta part veuiller se connecter avec votre compte {form.email.data}','success')
    return redirect(url_for("cas"))
@app.route('/listecas')
def listecas():
    cas=Cas.query.all()
    return render_template("listecas.html",cas=cas)
@app.route('/cas/<int:id>', methods=['GET', 'POST'])
def show(id):
    sommc =float 
    forme=DonnateurForm(request.form)
    cas=Cas.query.get(id)
    if request.form.get('valide') is not None:
        donnat=Donnateur(nom=forme.nom.data,prenom=forme.prenom.data,telephone=forme.telephone.data,email=forme.email.data)
        db.session.add(donnat)
        db.session.commit()
        don = Dons()
        don.montant = request.form.get('montant')
        don.donnateur_id=(donnat.id)
        don.cas_id=(cas.id)    
        detail = DetailleCas()
        det = DetailleCas()
        smc=float
        smr=float
        mnt=float
        det = DetailleCas.query.filter_by(cas_id=cas.id).first()
        smc =det.sommecollecter
        mnt=don.montant
        sommc=(float(smc)+float(mnt))
        db.session.add(don)
        db.session.commit()
        detail = DetailleCas.query.filter_by(cas_id=cas.id).update({'sommecollecter':sommc})
        smr=(float(cas.montant)-float(sommc))
        detail = DetailleCas.query.filter_by(cas_id=cas.id).update({'sommerestante':smr})
        db.session.commit()
        return redirect(url_for("listecas"))
    return render_template('show.html',cas=cas,forme=forme)
	#cas=Cas.query.get(id)
	#if not cas:
	    #abort(404)

@app.route('/detailcas/<int:id>')
def detailcas(id):
    detail = DetailleCas.query.filter_by(cas_id=id).first()
    return render_template("detailcas.html",detail=detail)   

@app.route('/don')
def don():
    forme=DonnateurForm(request.form)
    return render_template('don.html',forme=forme)

if __name__ =='__main__':
    #db.create_all()
    app.run(debug=True,port=3000)