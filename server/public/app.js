const nav = document.querySelector('nav');
const form = document.querySelector('form')
const allSurv = document.querySelector('#all-surveys');
const startSurv = document.querySelector('#start-survey');

//run
startSurv.style.display = 'none';
renderAllSurv();
nav.addEventListener('click', router);

function router(e) {
    e.preventDefault();
    if (e.target.tagName == 'A') {
        e.target.textContent == 'surveys' ? renderAllSurv() : renderStartSurv()
    }
}

//all surv logic
async function renderAllSurv() {
    allSurv.style.display = 'flex'
    allSurv.innerHTML = '';
    startSurv.style.display = 'none'
    try {
        const data = await fetchSurveys();
        data.forEach((record, indx) => {
            const item = survItemTempl(record, indx);
            allSurv.appendChild(item);
        });
    } catch (err) {
        console.log(err)
    }
}
async function fetchSurveys() {
    try {
        const res = await fetch('http://localhost:6161/data');
        if (!res.ok) {
            throw new Error();
        }
        const data = await res.json();
        return data;
    } catch (err) {
        alert('fetch error, check the server!');
        return
    }
}
function survItemTempl(record, indx) {
    const div = document.createElement('div');
    div.className = 'surv-item';
    div.innerHTML = `
                <p>Record ${indx}</p>
                <p>Name: ${record.name}</p>
                <p>Age: ${record.age}</p>
                <p>Info: ${record.info}</p>
            `
    return div;
}

//start surv logic
function renderStartSurv() {
    allSurv.style.display = 'none'
    startSurv.style.display = 'flex'
}

form.addEventListener('submit', submitForm);
async function submitForm(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const { name, age, info } = Object.fromEntries(formData);

    try {
        const res = await postSurvey(name, age, info);
        e.target.reset();
        startSurv.style.display = 'none';
        renderAllSurv();
    } catch (err) {
        console.log(err);
    }
}
async function postSurvey(name, age, info) {
    if (!name || !age || !info) {
        return
    }
    const headers = {
        'Content-Type': 'application/json'
    }
    const body = JSON.stringify({
        name: name.trim(),
        age: age.trim(),
        info: info.trim(),
    });
    try {
        const res = await fetch('http:localhost:6161/data', {
            method: 'post',
            headers,
            body
        });
    } catch (error) {
        alert('post error, check the server!');
        return
    }
}