import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import About from './Components/About';
import Layout from './Layout';
import Home from './Components/Home';
import "./App.css";



function App(){
  return (
   

    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="home" element={<Home />} />
          <Route path="about" element={<About />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>


  );
};


export default App;
