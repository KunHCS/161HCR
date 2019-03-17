import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import SignatureCanvas from 'react-signature-canvas';

class App extends Component {
  render() {
    return (
      <div>
      <h1>Handwriting Recognition</h1>
        <SignatureCanvas penColor='black'
    canvasProps={{width: 800, height: 800, className: 'sigCanvas'}} />
      </div>
    );
  }
}

export default App;
