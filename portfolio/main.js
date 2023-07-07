const body = document.body;
const scrollBtn = document.querySelector('#scrollBTN');
const menuBtn = document.querySelector('#mobile_menu');
const menu = document.querySelector('#mobile_dropdown');
const form = document.getElementById("contact_form");
const url = "https://portfolio-emailbackend.vercel.app/send"


form.addEventListener('submit', handleSubmit);

menuBtn.addEventListener('click', toggleMenu);

scrollBtn.addEventListener('click', returnToTop);

window.onscroll = () => { pageScroll() };


function toggleMenu() {
    menu.classList.toggle('hidden');
    menu.classList.toggle('flex');
    menu.classList.toggle('dropdown');
    menuBtn.classList.toggle('open');
    body.classList.toggle('no-scroll');
}


function returnToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

function pageScroll() {
    if (document.body.scrollTop > 320 || document.documentElement.scrollTop > 320) {
        scrollBtn.classList.remove('hidden');
    } else {
        scrollBtn.classList.add('hidden');
    }
}

async function handleSubmit(e) {
    e.preventDefault();

    const name = e.target.name.value;
    const email = e.target.email.value;
    const subject = e.target.subject.value;
    const content = e.target.content.value;

    if (name === '' || email === '' || subject === '' || content === '') {
        alert("Please fill all fields!");
        return;
    }

    try {
        let response = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                email: email,
                subject: subject,
                content: content
            }),
        })

        alert("Email sent successfully!");

    }
    catch (err) {
        console.log(err);
        alert("Something went wrong!");
    }

}