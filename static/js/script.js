let counter = 10;                                               // declaring of a local variable counter with the initial value 
const timeContainer = document.createElement('div');            // creating of the "div" element
let logo = document.querySelector('.navbar-brand');             // selecting the element with the class.
logo.after(timeContainer);                                      // inserting the "div" element after element logo.
function myTimer() {                                            // definding a function with the timer logic.
    console.log(counter);                                       // printing the value of counter in the browser console.
    counter--;                                                  // reducing the value of the counter by 1.
    timeContainer.innerText = `Your session will expire in ${counter} seconds`;             // insertion of the value of the counter in the "div" element.
    if (counter === 0) {                                        
        clearInterval(intervalId);
        console.log('Your session is over.')
        location.reload();                                      //refreshing the page after 10 seconds automatically.
    }
}
let intervalId = setInterval(myTimer, 1000);                    // 