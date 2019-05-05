import React, { Component } from 'react';
import './App.css';
import SignatureCanvas from 'react-signature-canvas';
import axios from 'axios';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      trimmedDataURL: null, result: '', value: 'HASYv2'
    };
    this.handleChange = this.handleChange.bind(this);
  }
  sigPad = {}
  clear = () => {
    this._signatureCanvas.clear()
  }
  trim = () => {
    this.setState({trimmedDataURL: this._signatureCanvas.getTrimmedCanvas()
      .toDataURL('image/png')});
    if (this.state.value === 'HASYv2') {this.predictImage(this._signatureCanvas.getTrimmedCanvas()
      .toDataURL('image/png'));}
    else {this.predictImage2(this._signatureCanvas.getTrimmedCanvas()
      .toDataURL('image/png'));}
  }

  // Predict using HASYv2 model
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

  // Predict using MNIST Model
  predictImage2 = (data) => {
  axios
    .post('http://127.0.0.1:5000/image2', data)
    .then(data => {
        this.setState({ 
          result: data.data.Result
        });
        console.log("Prediction MNIST: ", data.data.Result)})
    .catch(error => console.log(error.response));
  }

  // onChange for SELECT option
  handleChange(e) {
    this.setState({ value: e.target.value });
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
         <div>Model: 
         <select onChange={this.handleChange}>
           <option value="HASYv2">HASYv2</option>
           <option value="MNIST">MNIST</option>
          </select>
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
