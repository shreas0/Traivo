import '../CSS/InputBar.css';

function InputBar(){
    let greetings = 1;

    function CheckForSession(){
    if (greetings==1){
        const target= document.querySelector(".greetings");
        target.style.display= "none";
        greetings = 0;
        }
    }

    return(

        <div className="input">
            <input type="text" placeholder="Type something..."/>
            <button onClick={CheckForSession} >
                <div className='send-ico'></div>
            </button>
        </div>
    )
}

export default InputBar;