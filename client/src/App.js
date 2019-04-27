import React, { Component } from 'react';
import './App.css';
import SignatureCanvas from 'react-signature-canvas';
import axios from 'axios';


class App extends Component {
	state = {trimmedDataURL: null, result: ''}
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
    .post('http://127.0.0.1:5000/image', data)
    .then(data => {
        this.setState({ 
          result: data.data.Result
        });
        console.log("Prediction: ", data.data.Result)})
    .catch(error => console.log(error.response));
}


  render() {
  	let {trimmedDataURL, result} = this.state
    return (
      <div>
        <h1>Handwriting Recognition</h1>
          <div style={{border:'1px solid black', width:'300px', marginLeft:'5px'}}>
            <SignatureCanvas penColor='black' minWidth={3.0} maxWidth={3.0} 
             canvasProps={{width: 300, height: 300, className: 'sigCanvas'}} ref={(r) => { this._signatureCanvas = r;}} />
         </div>
         <div>
           <button  onClick={this.clear}>
              Clear
           </button>
           <button  onClick={this.trim}>
              Predict!
           </button>
        </div>
        <div>
           {result ? 'Prediction: '+result : ''}
        </div>
        <div>
        {trimmedDataURL
          ? <img alt="handwrittenText"
          src={trimmedDataURL} />
        : null}

        </div>
      </div>
      
    );
  }
}

export default App;
