import { BrowserRouter, Routes, Route } from 'react-router-dom';
import About from './Components/About';
import Layout from './Layout';
import Navbar from './Components/Navbar';
import Home from './Components/Home';



function App(){
  return (

    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/Home" element={<Home />} />
          <Route path="/About" element={<About />} />
        </Route>
      </Routes>
    </BrowserRouter>

  );
};


export default App;
