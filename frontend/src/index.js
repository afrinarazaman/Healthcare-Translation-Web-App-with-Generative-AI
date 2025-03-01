import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app';
import './index.css'; // optional, if you have custom styles or Tailwind CSS configured

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
