import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import Email from './Email';
import SaveUser from './components/SaveUser';
import { BrowserRouter, Routes, Route } from "react-router-dom";


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
       <Route path="/">
            <Route index  element={<SaveUser/>} /> 
            <Route path="Email" element={<Email/>} />
            <Route path="app" element={<App/>} />
       </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
