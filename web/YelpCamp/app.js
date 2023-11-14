// import all the packages
const express = require('express');
const mongoose = require('mongoose');
const path = require('path');

// set up configuration
if (process.env.NODE_ENV !== "production") {
    require('dotenv').config();
};

// set up database
const dbUrl = process.env.DB_URL;
mongoose.connect(dbUrl, {
    useNewUrlParser: true,
    // useCreateIndex: true,
    useUnifiedTopology: true
    // useFindAndModify: false
});
const db = mongoose.connection;
db.on("error", console.error.bind(console, "connection error:"));
db.once("open", () => {
    console.log("Database connected");
});

// create application
const app = express();

// set up middlewares
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// set up routes
app.get('/', (req, res) => {
    // res.send('HELLO FROM YELP CAMP!')
    res.render('home');
});

// set up application ports
app.listen(3000, () => {
    console.log('Serving on port 3000');
});
