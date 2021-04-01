import pymongo
from flask import Flask, render_template, redirect
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use pymongo to establish Mongo connection
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_app
collection = db.mars_scraped_data

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    
    # Find one record of data from the mongo database
    mars = list(db.mars_scraped_data.find())

    # Return template and data
    return render_template('index.html', mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars = scrape_mars.scrape()
    db.mars_scraped_data.drop()
    # Update the Mongo database using update and upsert=True
    db.mars_scraped_data.insert_one(mars)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)