import axios from 'axios'

import { 
    ORDER_CREATE_REQUEST,
    ORDER_CREATE_SUCCESS,
    ORDER_CREATE_FAIL,

    ORDER_DETAILS_REQUEST,
    ORDER_DETAILS_SUCCESS,
    ORDER_DETAILS_FAIL,

    ORDER_PAY_REQUEST,
    ORDER_PAY_SUCCESS,
    ORDER_PAY_FAIL,

    ORDER_LIST_MY_REQUEST,
    ORDER_LIST_MY_SUCCESS,
    ORDER_LIST_MY_FAIL,
} from '../constants/orderConstants'
import { domainURL } from '../constants/domainConstants'

import { CART_CLEAR_ITEMS } from '../constants/cartConstants'

import { csrftoken } from '../components/shared/Csrf'


export const createOrder = (order) => async (dispatch, getState) => {

    try {

        // userReducers.js case
        dispatch({
            type: ORDER_CREATE_REQUEST
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

        //console.log('Sending post request...', 'Csrftoken:', '| Authorization:', `Bearer ${userInfo.token}`)

        // Update the user data and store that in a variable 'data', which is fetched from the API via axios.
        // API takes in name, email and password.
        const { data } = await axios.post(
            `${domainURL}/api/v1/cart/add/`,
            order,
            config
        )
        .catch( (error) => console.log('axios post error:', error))

        //console.log('Returned data:', data)

        // Get the user data after making the API profile update call. Calls the reducer to update the state.
        dispatch({
            type: ORDER_CREATE_SUCCESS,
            payload: data
        })

        // After user has payed for the cart, clear it from the state.
        dispatch({
            type: CART_CLEAR_ITEMS,
            payload: data
        })

        // Remove the cart data from the local storage too.
        localStorage.removeItem('cartItems')

    }
    catch (error) {

        // Start product reducer with the specified case type
        dispatch({
            type: ORDER_CREATE_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail
            : error.message,
        })

    }
}

export const getOrderDetails = (id) => async (dispatch, getState) => {

    try {

        // userReducers.js case
        dispatch({
            type: ORDER_DETAILS_REQUEST
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

        // Get order/cart data from a created cart.
        const { data } = await axios.get(
            `${domainURL}/api/v1/cart/${id}/`,
            config
        )
        .catch( (error) => console.log('axios get error:', error))

        // Get the user data after making the API profile update call. Calls the reducer to update the state.
        dispatch({
            type: ORDER_DETAILS_SUCCESS,
            payload: data
        })

    }
    catch (error) {

        // Start product reducer with the specified case type
        dispatch({
            type: ORDER_DETAILS_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail
            : error.message,
        })

    }
}

export const payOrder = (id, paymentResult) => async (dispatch, getState) => {

    try {

        // userReducers.js case
        dispatch({
            type: ORDER_PAY_REQUEST
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

        // Get order/cart data from a created cart.
        const { data } = await axios.put(
            `${domainURL}/api/v1/cart/${id}/pay/`,
            paymentResult,
            config
        )
        .catch( (error) => console.log('axios post error:', error))

        // Get the user data after making the API profile update call. Calls the reducer to update the state.
        dispatch({
            type: ORDER_PAY_SUCCESS,
            payload: data
        })

    }
    catch (error) {

        // Start product reducer with the specified case type
        dispatch({
            type: ORDER_PAY_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail
            : error.message,
        })

    }
}



export const listMyOrders = () => async (dispatch, getState) => {

    try {

        // userReducers.js case
        dispatch({
            type: ORDER_LIST_MY_REQUEST
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

        // Get order/cart data from a created cart.
        const { data } = await axios.get(
            `${domainURL}/api/v1/my-orders/`,
            config
        )
        .catch( (error) => console.log('axios post error:', error))

        // Get the user data after making the API profile update call. Calls the reducer to update the state.
        dispatch({
            type: ORDER_LIST_MY_SUCCESS,
            payload: data
        })

    }
    catch (error) {

        // Start product reducer with the specified case type
        dispatch({
            type: ORDER_LIST_MY_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail
            : error.message,
        })

    }
}