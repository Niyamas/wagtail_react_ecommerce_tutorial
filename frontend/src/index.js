import React from 'react';
import ReactDOM from 'react-dom';

// Redux stuff
import { Provider } from 'react-redux'
import store from './store'


import './css/index.css';
import './bootstrap.min.css'

import App from './App';
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
/* 	<React.StrictMode>
		<App />
	</React.StrictMode>,
	document.getElementById('root') */

	// Use the Redux store globally throughout the app.
	<Provider store={store}>
		<App />
	</Provider>,
	document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
