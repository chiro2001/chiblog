import React from "react";
import './App.css';
import api from './api/api';

import Blackdrop from "./components/Blackdrop";


function App() {
  return (
    <div className="App">
      <button onClick={() => {
        api.requests.contentTree.get();
      }}>测试API</button>
      <br />
      <Blackdrop></Blackdrop>
    </div>
  );
}

export default App;
