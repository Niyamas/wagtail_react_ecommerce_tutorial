// Mainly Redux. Creates a store that holds the entire state tree of your app.
// It is closely linked with Redux's reducers.
// store.js is loaded on every page.

import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'

import { productListReducer, productDetailsReducer } from './reducers/productReducers'
import { cartReducer } from './reducers/cartReducers'
import { userLoginReducer } from './reducers/userReducers'


// Register reducers and collates them into a single constant.
// Should show up in the state.
const reducer = combineReducers({ 
    productList: productListReducer,
    productDetails: productDetailsReducer,
    cart: cartReducer,
    userLogin: userLoginReducer
})

// Pull cart data from local storage and parse it.
// Add conditional to check if the item still exists.
const cartItemsFromStorage = localStorage.getItem('cartItems') ? JSON.parse(localStorage.getItem('cartItems'))
    : []

// Pull user data from local storage and parse it.
// Add conditional to check if the data still exists.
const userInfoFromStorage = localStorage.getItem('userInfo') ? JSON.parse(localStorage.getItem('userInfo'))
    : null

// Set initial state, which has a number of values. Set the cart state to whatever is in local storage for the user with respect to their carts.
// Makes this data available for all pages.
const initialState = {
    cart: { cartItems: cartItemsFromStorage },
    userLogin: { userInfo: userInfoFromStorage }
}

// Define middleware as thunk, which interfaces with the redux devtools on Firefox.
const middleware = [thunk]

const store = createStore(
    reducer,
    initialState,
    composeWithDevTools(applyMiddleware(...middleware))
)

export default store