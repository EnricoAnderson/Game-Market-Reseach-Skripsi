const basicAuth = require('express-basic-auth')
const db = require('../database')

const login_auth = async (req, res, next) => {
    const db_data = await db.load_db()
    const username = req.query.username
    const password = req.query.password

    if(username && password) {
        console.log('Logged with ' + username + ' & ' + password)
        console.log('Admin [' + 'username: ' + db_data.username + ', password: ' + db_data.password + ']')
    
        const userMatches = basicAuth.safeCompare(username, db_data.username)
        const passwordMatches = basicAuth.safeCompare(password, db_data.password)

        if (userMatches && passwordMatches) {
            console.log('Basic Auth: Success')
            next()
        } else {
            console.log('Basic Auth: Failure')
            res.statusCode = 401
            res.redirect("/login?failedLogin=is-active")
        }
    } else {
        console.log('Procced to login page')
        res.redirect("/login")
    }

}

module.exports = login_auth 