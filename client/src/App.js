import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import SignatureCanvas from 'react-signature-canvas';

class App extends Component {
	state = {trimmedDataURL: null}
  sigPad = {}
  clear = () => {
    this._signatureCanvas.clear()
  }
  trim = () => {
    this.setState({trimmedDataURL: this._signatureCanvas.getTrimmedCanvas()
      .toDataURL('image/png')})
  }

  render() {
  	let {trimmedDataURL} = this.state
    return (
      <div>
      <h1>Handwriting Recognitionsss</h1>
        <SignatureCanvas penColor='black'
    canvasProps={{width: 800, height: 500, className: 'sigCanvas'}} ref={(r) => { this._signatureCanvas = r;}} />
      <div>
        <button  onClick={this.clear}>
          Clear
        </button>
        <button  onClick={this.trim}>
          Save
        </button>
      </div>
      {trimmedDataURL
        ? <img 
          src={trimmedDataURL} />
        : null}
      </div>
    );
  }
}

export default App;
