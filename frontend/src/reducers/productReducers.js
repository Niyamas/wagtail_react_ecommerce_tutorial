// Reducers are functions that tie actions and states together and allows them to interact.

import {
    PRODUCT_LIST_REQUEST,
    PRODUCT_LIST_SUCCESS,
    PRODUCT_LIST_FAIL,
    PRODUCT_DETAILS_REQUEST,
    PRODUCT_DETAILS_SUCCESS,
    PRODUCT_DETAILS_FAIL
} from '../constants/productConstants'


// Reducers initiate the state and changes the state according to the actions
// it receives from the actions that were dispatched.

export const productListReducer = (state = { products: [] }, action) => {
    
    // Depending on the action type, do something.
    switch(action.type) {

        // Case when products are loading.
        case PRODUCT_LIST_REQUEST:
            return { loading: true, products: [] }

        // Case when product loading is complete.
        case PRODUCT_LIST_SUCCESS:
            return { loading: false, products: action.payload }

        // Case when there is an error getting the products data.
        case PRODUCT_LIST_FAIL:
            return { loading: false, error: action.payload }

        default:
            return state
    }
}

export const productDetailsReducer = (state = { product: {reviews: []} }, action) => {
    
    // Depending on the action type, do something.
    switch(action.type) {

        // Case when products are loading.
        case PRODUCT_DETAILS_REQUEST:
            return { loading: true, ...state }

        // Case when product loading is complete.
        case PRODUCT_DETAILS_SUCCESS:
            return { loading: false, product: action.payload }

        // Case when there is an error getting the products data.
        case PRODUCT_DETAILS_FAIL:
            return { loading: false, error: action.payload }

        default:
            return state
    }
}