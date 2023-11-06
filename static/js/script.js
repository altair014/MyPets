let minutes = 1;
let seconds = 60;                                               // declaring of a local variable counter with the initial value 
const timeContainer = document.createElement('div');            // creating of the "div" element
timeContainer.setAttribute("class","link link-primary")
let logo = document.querySelector('.navbar-brand');             // selecting the element with the class.
logo.after(timeContainer);                                      // inserting the "div" element after element logo.
function myTimer() {                                            // definding a function with the timer logic.
    if (seconds < 10){
        timeContainer.innerText = `Your session will expire in 0${minutes}:0${seconds}`;             // insertion of the value of the counter in the "div" element.
    } 
    else{
        timeContainer.innerText = `Your session will expire in 0${minutes}:${seconds}`;
    }
    
    console.log(seconds);                                       // printing the value of counter in the browser console.
    if (minutes === 0 && seconds === 0) {                                        
        clearInterval(intervalId);
        console.log('Your session is over.')
        location.reload();                                      //refreshing the page after 10 seconds automatically.
    }

    
    
    if (seconds === 0) {
        if (minutes !== 0) {
            minutes--;
        }
        seconds = 60;                                                                             
    }
    seconds--;                                                  // reducing the value of the counter by 1.
}
let intervalId = setInterval(myTimer, 1000);                    // 