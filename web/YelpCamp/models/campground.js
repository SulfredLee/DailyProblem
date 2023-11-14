const mongoose = require('mongoose');
const Schema = mongoose.Schema; // now we can use a short hand. Instead of mongoose.Schema.xxxxx . We can use xxxxx directly

const CampgroundSchema = new Schema({
    title: String,
    price: String,
    description: String,
    location: String
});

module.exports = mongoose.model('Campground', CampgroundSchema);
