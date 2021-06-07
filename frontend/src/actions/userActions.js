// After being dispatched, the action will update the state and do other logic.

import axios from 'axios'

import { 
    USER_LOGIN_REQUEST,
    USER_LOGIN_SUCCESS,
    USER_LOGIN_FAIL,
    USER_LOGOUT
} from '../constants/userConstants'

import { csrftoken } from '../components/shared/Csrf'


export const login = (email, password) => async (dispatch) => {

    try {

        dispatch({
            type: USER_LOGIN_REQUEST
        })

        console.log('csrftoken:', csrftoken)

        // Send additional data to the API call.
        const config = {

            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        }

        // Make API call to the JWT login with the user's username (email) and password
        const {data} = await axios.post(
            'http://localhost:8000/api/v1/users/login/',
            {'username': email, 'password': password },
            config
        )

        // Get the user data after making the API login call.
        dispatch({
            type: USER_LOGIN_SUCCESS,
            payload: data
        })

        // Save the user data to the user's browser local storage.
        localStorage.setItem('userInfo', JSON.stringify(data))

    }
    catch(error) {

        // Start product reducer with the specified case type
        dispatch({
            type: USER_LOGIN_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail
            : error.message,
        })

    }

}