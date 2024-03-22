import React,{useState} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

const App = () => {
  const [text, setText] = useState('');
  const [summarizedText, setSummarizedText] = useState('');
  const [selectedModel, setSelectedModel] = useState('model1')
  const [selectedLength, setSelectedLength] = useState('short')
  const [url, setUrl] = useState('')

  const countWords = (str='') => {
    return str.split(/\s+/).filter(Boolean).length;
  };

  const handleUrlChange = (e)=> {
    const inputUrl = e.target.value;
    setUrl(inputUrl);
    setText('');
  }
 
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    const requestBody = url ? {url,selectedModel,selectedLength} : {text,selectedModel,selectedLength};
    const response = await fetch('/',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // body: JSON.stringify({text,selectedModel,selectedLength,url}),
      body: JSON.stringify(requestBody),
    });
    const data = await response.json();
    console.log('Response data:',data);
    setText(data.formatted_text);
    setSummarizedText(data.summarized_text);
  };
  


return (
  <>
  <div className="col text-center mb-5 bg-success">
    <h1 className="display-4" style={{color:'white'}}>Nepali News Summarizer</h1>
  </div>
    <div className="container">
      
      <div className="row mb-3 align-items-center">
      
        <div className="col-md-5 d-flex justify-content-start">
          <p className="mb-0">Input Text Word Count: {countWords(text)}</p>
        </div>
            <div className="col d-flex justify-content-end">
            <div style={{marginRight: 10}}>
              <label htmlFor="modelSelect" className="form-label">Select Model</label>
              <select 
                id="modelSelect" 
                className="form-select" 
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
              >
                <option value="model1">mT5</option>
                <option value="model2">MBART</option>
              </select>
            </div>
            <div>
              <label htmlFor="LengthSelect" className="form-label">Select Length</label>
              <select 
                id="lengthSelect" 
                className="form-select" 
                value={selectedLength}
                onChange={(e) => setSelectedLength(e.target.value)}
              >
                <option value="short">Short </option>
                <option value="long">Long</option>
              </select>
            </div>
          </div>
      </div>
      <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor='urlInput' className="form-label">Enter URL:</label>
        <input 
        type="text"
        id='urlInput'
        className='form-control'
        placeholder='Enter URL here...'
        value={url}
        onChange={handleUrlChange}
        >
        
        </input>
        </div>
        <div className="mb-3">
          <textarea
            className="form-control"
            placeholder="Enter News Article to summarize..."
            rows="8"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </div>
        <div className="d-flex justify-content-between">
          <button type="submit" className="btn btn-success">
            Summarize
          </button>
        
        </div>
      </form>
      {summarizedText && (
        <div className="row mt-4">
          <div className="col">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">Summarized Text:</h5>
                <p className="card-text">{summarizedText}</p>
              </div>
            </div>
          </div>
          
            <p className="mt-3">Summary Word Count: {countWords(summarizedText)}</p>
          
        </div>
      )}
    </div>
  </>
);
};

export default App