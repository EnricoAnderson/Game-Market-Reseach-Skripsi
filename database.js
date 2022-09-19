const { JsonDB } = require('node-json-db')
const { Config } = require('node-json-db/dist/lib/JsonDBConfig')

async function create_db() {
    try {
        console.log('Creating default database...')
        var db = new JsonDB(new Config("db_conf", true, true, '/'));
        await db.push("/last_update","01-01-2022");
        await db.push("/username","admin");
        await db.push("/password","admin");
    
        console.log('Default database created!')
        console.log(await db.getData("/"))
    
        return db
    } catch(error) {
        console.log(error)
    }
}

async function save_admin(data) {
    try {
        console.log('Saving to the database...')
        var db = new JsonDB(new Config("db_conf", true, true, '/'));
        await db.push("/username", data.username);
        await db.push("/password", data.password);
        db.save()
        console.log('Succesfully saved to the database!')
    } catch (error) {
        console.log(error)
    }
}

async function save_date(data) {
    try {
        console.log('Saving to the database...')
        var db = new JsonDB(new Config("db_conf", true, true, '/'));
        await db.push("/last_update", data);
        db.save()
        console.log('Succesfully saved to the database!')
    } catch (error) {
        console.log(error)
    }
}

async function load_db() {
    try {
        console.log('Loading database...')
        var db = new JsonDB(new Config("db_conf", true, true, '/'));
        var data = await db.getData("/")
        console.log('Succesfully loading root data!')
        return data
    } catch (error) {
        console.log(error)
    }
}

module.exports.create_db = create_db
module.exports.save_admin = save_admin
module.exports.save_date = save_date
module.exports.load_db = load_db