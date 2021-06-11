import axios from 'axios'

import { 
    ORDER_CREATE_REQUEST,
    ORDER_CREATE_SUCCESS,
    ORDER_CREATE_FAIL
} from '../constants/orderConstants'

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

        // Update the user data and store that in a variable 'data', which is fetched from the API via axios.
        // API takes in name, email and password.
        const { data } = await axios.post(
            'http://localhost:8000/api/v1/cart/add/',
            order,
            config
        )

        // Get the user data after making the API profile update call. Calls the reducer to update the state.
        dispatch({
            type: ORDER_CREATE_SUCCESS,
            payload: data
        })

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