from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

from sqlalchemy.orm.exc import UnmappedInstanceError

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

SECRET_KEY = 'secure_key'

# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        # dictionary = {}
        # Loop through each column in the data record
        # for column in self.__table__.columns:
        #     # Create a new dictionary entry;
        #     # where the key is the name of the column
        #     # and the value is the value of the column
        #     dictionary[column.name] = getattr(self, column.name)
        # return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()





@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_cafe():
    result = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = random.choice(result)
    # print(random_cafe.name)

    return jsonify(cafe = random_cafe.to_dict())
# GET - All Records
@app.route("/all")
def all_cafe():
    result = db.session.execute(db.select(Cafe)).scalars().all()
    all_cafes = [cafe.to_dict() for cafe in result]
    return  jsonify(all_cafes)

@app.route('/search')
def search():
    loc = request.args.get('loc', None)
    if not loc:
        return jsonify(error={"Bad Request": "Please provide a loc query parameter."}), 400

    # fetch all cafes whose location exactly matches loc
    result = (
        db.session
          .execute(db.select(Cafe).where(Cafe.location == loc))
          .scalars()
          .all()
    )

    if result:
        return jsonify(cafes=[c.to_dict() for c in result]), 200
    else:
        return (
            jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}),
            404
        )

# HTTP POST - Create Record
@app.route('/add',methods=['POST'])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})
# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:cafe_id>',methods=['PATCH'])
def update_price_by_id(cafe_id):
    new_price = request.args.get('new_price')
    try:
        price_to_update = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        price_to_update.coffee_price = new_price
        db.session.commit()
    except AttributeError:
        return jsonify({'error':{
            'Not found': "No cafe with that id"
        }})

    return jsonify({"success": "Successfully updated the price"})

# HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    # 1) auth
    api_key = request.args.get('api_key')
    if api_key != SECRET_KEY:
        return jsonify(error="You are not authorised"), 403

    # 2) lookup
    cafe = db.session.get(Cafe, cafe_id)
    if not cafe:
        return jsonify(error=f"No cafe found with id={cafe_id}"), 404

    # 3) delete & commit
    try:
        db.session.delete(cafe)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(error="Database error deleting cafe", details=str(e)), 500

    # 4) all good
    return jsonify(success=f"Cafe id={cafe_id} deleted"), 200

if __name__ == '__main__':
    app.run(debug=True)
