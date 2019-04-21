import React, { Component } from 'react';
import './App.css';
import SignatureCanvas from 'react-signature-canvas';
import axios from 'axios';





class App extends Component {
	state = {trimmedDataURL: null}
  sigPad = {}
  clear = () => {
    this._signatureCanvas.clear()
  }
  trim = () => {
    this.setState({trimmedDataURL: this._signatureCanvas.getTrimmedCanvas()
      .toDataURL('image/png')});
    this.predictImage(this._signatureCanvas.getTrimmedCanvas()
      .toDataURL('image/png'));
  }

  predictImage = (data) => {
  axios
    .post('image', data);
  
}


  render() {
  	let {trimmedDataURL} = this.state
    return (
      <div>
      <h1>Handwriting Recognition</h1>
        <SignatureCanvas penColor='black'
    canvasProps={{width: 500, height: 500, className: 'sigCanvas'}} ref={(r) => { this._signatureCanvas = r;}} />
      <div>
        <button  onClick={this.clear}>
          Clear
        </button>
        <button  onClick={this.trim}>
          Save
        </button>
      </div>
      {trimmedDataURL
        ? <img alt="handwrittenText"
          src={trimmedDataURL} />
        : null}
      </div>
    );
  }
}

export default App;
