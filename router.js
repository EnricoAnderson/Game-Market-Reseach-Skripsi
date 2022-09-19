const express = require('express');
const router = express.Router();
const processor = require('./processor')
const fs = require("fs");
const login_auth = require('./middlware/authMiddleware')
const db = require('./database');
const { equal } = require('assert');

const GENRETOP10_PATH = "pymodule\\genretop10.json"
const REKOMENDASI_PATH = "pymodule\\rekomendasi.json"

router.get("/", async function (req, res) {
    try {
        res.render("index");
    } catch (error) {
        console.log(error)
    }
})

router.get("/result", async function (req, res) {
    try {

        var genretop10 = JSON.parse(fs.readFileSync(GENRETOP10_PATH, 'utf8'));
        var rekomendasi = JSON.parse(fs.readFileSync(REKOMENDASI_PATH, 'utf8'));

        res.render("result", {
            genre: genretop10.genre,
            revenue: genretop10.revenue,
            revenue_total: genretop10.total,
            rekomendasi: rekomendasi
        });
    } catch (error) {
        console.log(error)
    }
})

router.get("/login", async function (req, res) {
    try {
        res.render("login");
    } catch (error) {
        console.log(error)
    }
})

router.post("/login", async function (req, res) {
    try {
        var username = req.body.username
        var password = req.body.password
        console.log(username)
        res.redirect('/admin?username=' + username + '&password=' + password)
    } catch (error) {
        console.log(error)
    }
})

router.get("/admin", login_auth, async (req, res) => {
    try {
        db_data = await db.load_db()

        res.render("admin", {
            username: db_data.username,
            password: db_data.password,
            last_update: db_data.last_update
        })
    } catch(error) {
        console.log(error)
        res.redirect("/login?failedLogin=is-active")
    }
})

router.post("/save", async function (req, res) {
    try {

        await db.save_admin(req.body)
        console.log("Succesfully updated admin data!")
        res.redirect('/admin?username=' + req.body.username + '&password=' + req.body.password)
    } catch (error) {
        console.log(error)
    }
})

router.post("/scraper", async function (req, res) {
    try {
        console.log("Trying to scrape...")
        var page = req.body.pageTotal
        var output = await processor.start_scraper(page)
        console.log(output)
        
        if(output.includes("[SUCCESS]")) {
            // Scraping success
            var today = new Date();
            var dd = String(today.getDate()).padStart(2, '0');
            var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
            var yyyy = today.getFullYear();

            today = mm + '/' + dd + '/' + yyyy;
            db.save_date(today)
            console.log("Succesfully scraped new data!")
        } else if (output.includes("[ERROR]")) {
            // Scraping failed
            console.log("Failed to scrape new data")
        } else {
            // Anyelse
            console.log("Error unknown")
        }

        res.redirect('back')
    } catch (error) {
        console.log(error)
    }
})

router.post("/process", async function (req, res) {
    try {
        console.log("Trying to process data...")
        var genreInput = req.body.genreInput
        var suppInput = req.body.suppInput
        var confInput = req.body.confInput
        var panjInput = req.body.panjangRekomendasi

        var output = await processor.start_process(genreInput, suppInput, confInput, panjInput)

        if(output.includes("[SUCCESS]")) {
            // Process success
            console.log("Succesfully process data!")
            res.redirect("/result")
        } else if (output.includes("[ERROR]")) {
            // Process failed
            console.log("Failed to process data")
        } else {
            // Anyelse
            console.log("Error unknown")
        }
    } catch (error) {
        console.log(error)
    }
})

module.exports = router;