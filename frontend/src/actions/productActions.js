// After being dispatched, the action will update the state and do other logic.

import axios from 'axios'

import {
    PRODUCT_LIST_REQUEST,
    PRODUCT_LIST_SUCCESS,
    PRODUCT_LIST_FAIL,
    PRODUCT_DETAILS_REQUEST,
    PRODUCT_DETAILS_SUCCESS,
    PRODUCT_DETAILS_FAIL
} from '../constants/productConstants'


// In charge of replacing the API call in the homescreen
export const listProducts = () => async (dispatch) => {

    try {

        // Start product reducer with the specified case type
        dispatch({
            type: PRODUCT_LIST_REQUEST
        })

        // Fetch the API items data with axios
        const { data } = await axios.get('http://localhost:8000/api/v1/items/')

        // Start product reducer with the specified case type
        dispatch({
            type: PRODUCT_LIST_SUCCESS,
            payload: data
        })
    }
    catch(error) {

        // Start product reducer with the specified case type
        // Detail comes from the error message from api.views.UserCreateView() and is a custom message.
        dispatch({
            type: PRODUCT_LIST_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail : error.message,

        })
    }
}

// In charge of replacing the API call in the item detail page
export const listProductDetails = (id) => async (dispatch) => {

    try {

        // Start product reducer with the specified case type
        dispatch({
            type: PRODUCT_DETAILS_REQUEST
        })

        // Fetch the API items data with axios
        const { data } = await axios.get(`http://localhost:8000/api/v1/item/${id}`)

        // Start product reducer with the specified case type
        dispatch({
            type: PRODUCT_DETAILS_SUCCESS,
            payload: data
        })
    }
    catch(error) {

        // Start product reducer with the specified case type
        dispatch({
            type: PRODUCT_DETAILS_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail
            : error.message,
        })
    }
}