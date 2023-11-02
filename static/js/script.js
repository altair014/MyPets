let counter = 20;
const timeContainer = document.createElement('div');
let logo = document.querySelector('.navbar-brand');
logo.after(timeContainer);
function myTimer() {
    console.log(counter);
    counter--;
    timeContainer.innerText = `${counter} seconds`;
    if (counter === 0) {
        clearInterval(intervalId);
        console.log('Your session is over.')
        location. reload();
    }
}
let intervalId = setInterval(myTimer, 1000);

