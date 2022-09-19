const express = require("express");
const app = express();
const router = require('./router');
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true })); 
app.use('/', router)
app.use(express.static("public"))
app.set("view engine", "ejs");

app.listen(port, function () {
  console.log('Server is running on PORT',port);
});
