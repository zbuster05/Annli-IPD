import './App.css';
import React from 'react';
import Header from "./Header.jsx";
import { useState, useEffect } from 'react';



const App = () => {
  
  const [modeSelected, setModeSelected] = useState(false);
  const [testMode, setTestMode] = useState(false);

  useEffect(() => {
    setModeSelected(false)
  }, [])
  
  return (
    <div className="App">
      <Header/>
      {modeSelected ? (
        <>
        <button onClick={() => setModeSelected(false)}>Back</button>
        </>
      ) : (
        <>
        <button onClick={() => setModeSelected(true)}>Test a Strategy</button>
        <button onClick={() => setModeSelected(true)}>Submit a Strategy</button>
        </>
      )}
    </div>
  );
}

export default App;
