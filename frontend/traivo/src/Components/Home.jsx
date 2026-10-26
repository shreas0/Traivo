import InputBar from "./InputBar";
import OutputPlain from "./OutputPlain";
function Home(){
    return(
        <div className="main" style={{ minHeight: 'calc(100vh - 40px)', display: 'flex', flexDirection: 'column' }}>
        <OutputPlain/>
        <footer>
            <InputBar/>
        </footer>
        </div>
    )
}

export default Home;
