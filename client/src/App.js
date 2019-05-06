import React, { Component } from "react";
import "./App.css";
import SignatureCanvas from "react-signature-canvas";
import axios from "axios";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      trimmedDataURL: null,
      result: "",
      value: "HASYv2"
    };
    this.handleChange = this.handleChange.bind(this);
  }
  sigPad = {};
  clear = () => {
    this._signatureCanvas.clear();
  };
  trim = () => {
    this.setState({
      trimmedDataURL: this._signatureCanvas.toDataURL("image/png")
    });
    if (this.state.value === "HASYv2") {
      this.predictImage(
        this._signatureCanvas.getTrimmedCanvas().toDataURL("image/png")
      );
    } else {
      this.predictImage2(this._signatureCanvas.toDataURL("image/png"));
    }
  };

  // Predict using HASYv2 model
  predictImage = data => {
    axios
      .post("http://127.0.0.1:5000/image", data)
      .then(data => {
        this.setState({
          result: data.data.Result
        });
        console.log("Prediction: ", data.data.Result);
      })
      .catch(error => console.log(error.response));
  };

  // Predict using MNIST Model
  predictImage2 = data => {
    axios
      .post("http://127.0.0.1:5000/image2", data)
      .then(data => {
        this.setState({
          result: data.data.Result
        });
        console.log("Prediction MNIST: ", data.data.Result);
      })
      .catch(error => console.log(error.response));
  };

  // onChange for SELECT option
  handleChange(e) {
    this.setState({ value: e.target.value });
  }

  render() {
    let { trimmedDataURL, result } = this.state;
    return (
      <div>
        <div className="container">
          <div className="row">
            <div className="col-md-7 mt-4 mx-auto">
              <h1 className="text-center">Handwriting Recognition</h1>
              <div
                className="mx-auto mt-3"
                style={{
                  border: "1px solid black",
                  width: "300px",
                  marginLeft: "5px"
                }}
              >
                <SignatureCanvas
                  penColor="black"
                  minWidth={3.0}
                  maxWidth={3.0}
                  canvasProps={{
                    width: 300,
                    height: 300,
                    className: "sigCanvas"
                  }}
                  ref={r => {
                    this._signatureCanvas = r;
                  }}
                />
              </div>
              <div className="mt-2 ml-5">
                Model:
                <br />
                <select onChange={this.handleChange}>
                  <option value="HASYv2">HASYv2</option>
                  <option value="MNIST">MNIST</option>
                </select>
              </div>
              <div className="mt-2 ml-5">
                <button className="btn btn-secondary" onClick={this.clear}>
                  Clear
                </button>
                <button className="btn ml-2 btn-success" onClick={this.trim}>
                  Predict!
                </button>
              </div>
              <div className="ml-5 mt-2"><h1>{result ? "Prediction: " + result : ""}</h1></div>
              <div className="ml-5">
                {trimmedDataURL ? (
                  <img alt="handwrittenText" src={trimmedDataURL} />
                ) : null}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
