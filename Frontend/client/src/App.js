// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;


import React,{useState} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

const App = () => {
  const [text, setText] = useState('');
  const [summarizedText, setSummarizedText] = useState('');
  const [selectedModel, setSelectedModel] = useState('model1')

  // const handleSubmit = async (e) => {
  //   e.preventDefault();
  //   const response = await fetch('/',{
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     body: JSON.stringify({text,selectedModel}),
  //   });
  //   const data = await response.json()
  //   setSummarizedText(data.summarized_text);
  // };


  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({text,selectedModel}),
    });
    const data = await response.json()
    setSummarizedText(data.summarized_text);
  };
  
  // return (
  //   <div >
  //     <h1 className='justify-center'>Text Summarizer</h1>
  //     <form onSubmit={handleSubmit}>
  //       <textarea value={text} onChange={(e) => setText(e.target.value)} />
  //       <button type="submit">Summarize</button>
  //     </form>
  //     {summarizedText && (
  //       <div>
  //         <h2>Summarized Text:</h2>
  //         <p>{summarizedText}</p>
  //       </div>
  //     )}
  //   </div>
  // )

  // return (
  //   <div className="bg-gray-100 min-h-screen flex flex-col items-center justify-center py-8">
  //     <h1 className="text-3xl font-bold mb-8">Text Summarizer</h1>
  //     <form onSubmit={handleSubmit} className="w-full max-w-md px-4">
  //       <textarea
  //         className="w-full border border-black-300 rounded p-2 mb-4"
  //         rows="6"
  //         value={text}
  //         onChange={(e) => setText(e.target.value)}
  //         placeholder="Enter text to summarize..."
  //       />
  //       <button
  //         type="submit"
  //         className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
  //       >
  //         Summarize
  //       </button>
  //     </form>
  //     {summarizedText && (
  //       <div className="mt-8">
  //         <h2 className="text-xl font-semibold mb-2">Summarized Text:</h2>
  //         <p className="bg-white border border-gray-300 rounded p-4">{summarizedText}</p>
  //       </div>
  //     )}
  //   </div>
  // )

  // return (
  //   <div className="bg-gray-100 min-h-screen flex flex-col items-center justify-center py-8">
  //     <h1 className="text-3xl font-bold mb-8">Text Summarizer</h1>
  //     <form onSubmit={handleSubmit} className="w-full max-w-md px-4">
  //       <textarea
  //         className="w-full border border-gray-300 rounded-md p-2 mb-4 h-40 resize-none focus:border-blue-500"
  //         value={text}
  //         onChange={(e) => setText(e.target.value)}
  //         placeholder="Enter text to summarize..."
  //       />
  //       <button
  //         type="submit"
  //         className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
  //       >
  //         Summarize
  //       </button>
  //     </form>
  //     {summarizedText && (
  //       <div className="mt-8">
  //         <h2 className="text-xl font-semibold mb-2">Summarized Text:</h2>
  //         <p className="bg-white border border-gray-300 rounded p-4">{summarizedText}</p>
  //       </div>
  //     )}
  //   </div>
  // );
//   return (
//     <div className="container">
//       <h1 className="heading">Text Summarizer</h1>
//       <form onSubmit={handleSubmit}>
//         <textarea
//           className="textarea"
//           value={text}
//           onChange={(e) => setText(e.target.value)}
//           placeholder="Enter text to summarize..."
//         />
//         <button type="submit" className="button">
//           Summarize
//         </button>
//       </form>
//       {summarizedText && (
//         <div>
//           <h2>Summarized Text:</h2>
//           <p>{summarizedText}</p>
//         </div>
//       )}
//     </div>
//   );

// }

// // export default App

// return (
//   <div className="container">
//     <div className="row">
//       <div className="col text-center mb-4">
//         <h1 className="display-4">Nepali News Summarizer</h1>
//       </div>
//     </div>
//     <div className="row">
//       <div className="col">
//         <form onSubmit={handleSubmit}>
//           <div className="mb-3">
//             <textarea
//               className="form-control"
//               value={text}
//               onChange={(e) => setText(e.target.value)}
//               placeholder="Enter text to summarize..."
//               rows="5" // Adjust the number of rows as needed
//             />
//           </div>
//           <button type="submit" className="btn btn-primary">
//             Summarize
//           </button>
//         </form>
//       </div>
//     </div>
//     {summarizedText && (
//       <div className="row mt-4">
//         <div className="col">
//           <h2>Summarized Text:</h2>
//           <p className="lead">{summarizedText}</p>
//         </div>
//       </div>
//     )}
//   </div>
// );


return (
  <>
  
  <div className="container">
    <div className="row">
      <div className="col text-center mb-4">
        <h1 className="display-4">Nepali News Summarizer</h1>
      </div>
    </div>
    <div className="row">
      <div className="col-md-3]">
        <div className="mb-3">
          <label htmlFor="modelSelect" className="form-label">Select Model</label>
          <select 
            id="modelSelect" 
            className="form-select" 
            defaultValue="default"
            // disabled // Disable the dropdown menu
            onChange={(e)=> setSelectedModel(e.target.value)}
            style={{width:'150px'}}
          >
            <option value="default">mT5</option>
            <option value="model2">MBART</option>
            
            {/* Add more options for different models */}
          </select>
        </div>
      </div>
      </div>
      <div className='row'>
      <h2>News Article:</h2>
      <div className="col">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <textarea
              className="form-control"
              placeholder="Enter text to summarize..."
              rows="5"
              value={text}
              onChange={(e) => setText(e.target.value)}

            />
          </div>
          <button type="submit" className="btn btn-primary"> {/* Disable the button */}
            Summarize
          </button>
        </form>
      </div>
      </div>
    {summarizedText && (  
    <div className="row mt-4">
      <div className="col">
        <h2>Summarized Text:</h2>
        <p className="lead">{summarizedText}</p>
      </div>
    </div>
    )
}
  </div>
  </>
);
    }

export default App