// After being dispatched, the action will update the state and do other logic.

import axios from 'axios'

import {
    PRODUCT_LIST_REQUEST,
    PRODUCT_LIST_SUCCESS,
    PRODUCT_LIST_FAIL,

    PRODUCT_DETAILS_REQUEST,
    PRODUCT_DETAILS_SUCCESS,
    PRODUCT_DETAILS_FAIL,
    
    PRODUCT_CREATE_REVIEW_REQUEST,
    PRODUCT_CREATE_REVIEW_SUCCESS,
    PRODUCT_CREATE_REVIEW_FAIL,

    PRODUCT_TOP_REQUEST,
    PRODUCT_TOP_SUCCESS,
    PRODUCT_TOP_FAIL,
} from '../constants/productConstants'
import { domainURL } from '../constants/domainConstants'

import { csrftoken } from '../components/shared/Csrf'


// In charge of replacing the API call in the homescreen
export const listProducts = (keyword = '') => async (dispatch) => {

    try {

        // Start product reducer with the specified case type
        dispatch({
            type: PRODUCT_LIST_REQUEST
        })

        // Fetch the API items data with axios
        const { data } = await axios.get(`${domainURL}/api/v1/items/${keyword}`)

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
        const { data } = await axios.get(`${domainURL}/api/v1/item/${id}`)

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

//
export const createProductReview = (productId, review) => async (dispatch, getState) => {

    try {

        // Dispatch the request, which will return loading=true
        dispatch({
            type: PRODUCT_CREATE_REVIEW_REQUEST
        })

        // Get from the state userInfo, which will get the JWT access token in the config variable.
        const { userLogin: { userInfo } } = getState()

        // Send additional headers data to the API call.
        const config = {

            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
                Authorization: `Bearer ${userInfo.token}`
            }
        }

        // Send POST review data to the API for serialization and object saving to the database.
        await axios.post(
            `${domainURL}/api/v1/item/${productId}/reviews/`,
            review,
            config
        )

        // Dispatch the success action and pass on the data via the payload
        dispatch({
            type: PRODUCT_CREATE_REVIEW_SUCCESS,
            //payload: data       // @ todo: this is not needed? Reducer doesn't take in data
        })

    }
    catch (error) {

        // Start product reducer with the specified case type
        dispatch({
            type: PRODUCT_CREATE_REVIEW_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail
            : error.message,
        })
    }

}

export const listTopProducts = () => async (dispatch) => {

    try {

        // Start product reducer with the specified case type
        dispatch({
            type: PRODUCT_TOP_REQUEST
        })

        // Fetch the API items data with axios
        const { data } = await axios.get(`${domainURL}/api/v1/items/top/`)

        // Start product reducer with the specified case type
        dispatch({
            type: PRODUCT_TOP_SUCCESS,
            payload: data
        })
    }
    catch(error) {

        // Start product reducer with the specified case type
        // Detail comes from the error message from api.views.UserCreateView() and is a custom message.
        dispatch({
            type: PRODUCT_TOP_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail : error.message,

        })
    }
}