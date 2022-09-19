const { spawn } = require("child_process");
const { once } = require('events');

async function start_scraper(page) {
    const pyProg = spawn('.\\venv\\Scripts\\python.exe', ['pymodule\\start_scraper.py', page]);
    var output = '';

    pyProg.stdin.setEncoding = 'utf-8';

    pyProg.stdout.on('data', (data) => {
        output += data.toString();
    });

    pyProg.stderr.on('data', (data) => {
        console.log('error:' + data);
    });

    await once(pyProg, 'close')
    console.log(output)
    return output;
}

async function start_process(genre, supp, conf, panj) {
    const pyProg = spawn('.\\venv\\Scripts\\python.exe', ['pymodule\\start_reccomendation.py', genre, supp, conf, panj]);
    var output = '';

    pyProg.stdin.setEncoding = 'utf-8';

    pyProg.stdout.on('data', (data) => {
        output += data.toString();
    });

    pyProg.stderr.on('data', (data) => {
        console.log('error:' + data);
    });

    await once(pyProg, 'close')
    console.log(output)
    return output;
}

module.exports.start_scraper = start_scraper;
module.exports.start_process = start_process;