// After being dispatched, the action will update the state and do other logic.

import axios from 'axios'

import { 
    USER_LOGIN_REQUEST,
    USER_LOGIN_SUCCESS,
    USER_LOGIN_FAIL,
    USER_LOGOUT,

    USER_REGISTER_REQUEST,
    USER_REGISTER_SUCCESS,
    USER_REGISTER_FAIL,

    USER_DETAILS_REQUEST,
    USER_DETAILS_SUCCESS,
    USER_DETAILS_FAIL,
    USER_DETAILS_RESET,

    USER_UPDATE_PROFILE_REQUEST,
    USER_UPDATE_PROFILE_SUCCESS,
    USER_UPDATE_PROFILE_FAIL,
    //USER_UPDATE_PROFILE_RESET
} from '../constants/userConstants'

import { csrftoken } from '../components/shared/Csrf'


export const login = (email, password) => async (dispatch) => {

    try {

        dispatch({
            type: USER_LOGIN_REQUEST
        })

        // Send additional data to the API call.
        const config = {

            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        }

        // Make API call to the JWT login with the user's username (email) and password
        const { data } = await axios.post(
            'http://localhost:8000/api/v1/users/login/',
            {'username': email, 'password': password},
            config
        )

        console.log('login data:', data)

        // Get the user data after making the API login call.
        dispatch({
            type: USER_LOGIN_SUCCESS,
            payload: data
        })

        // Save the user data to the user's browser local storage.
        localStorage.setItem('userInfo', JSON.stringify(data))

    }
    catch (error) {

        // Start product reducer with the specified case type
        dispatch({
            type: USER_LOGIN_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail
            : error.message,
        })

    }
}


export const logout = () => (dispatch) => {

    // Log the user out by removing the userInfo from the local storage.
    // Need to also update the state (done in userReducers.js).
    localStorage.removeItem('userInfo')

    // Send signal to userReducer to update the state by emptying the userInfo variable there.
    dispatch({
        type: USER_LOGOUT
    })

    // Send signal to userReducer to empty the state after logging out.
    // Prevents the bug that after logging out, the previous logged-in user's
    // information will be displayed in the profile of the new logged in user!
    dispatch({
        type: USER_DETAILS_RESET
    })
}


export const register = (name, email, password) => async (dispatch) => {

    try {

        dispatch({
            type: USER_REGISTER_REQUEST
        })

        // Send additional headers data to the API call.
        const config = {

            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        }

        // Make API call to the JWT register with the user's name, email, and password.
        // Due to view logic, will split two names as first_name and last_name. If one
        // is given, leave last_name blank and fill in first_name.
        const {data} = await axios.post(
            'http://localhost:8000/api/v1/users/register/',
            { 'name': name, 'email': email, 'password': password },
            config
        )

        console.log('register data = ', data)

        // Get the user data after making the API login call.
        dispatch({
            type: USER_REGISTER_SUCCESS,
            payload: data
        })

        // Login the user immediately after registering.
        dispatch({
            type: USER_LOGIN_SUCCESS,
            payload: data
        })

        // Save the user data to the user's browser local storage.
        localStorage.setItem('userInfo', JSON.stringify(data))

    }
    catch (error) {

        // Start product reducer with the specified case type
        dispatch({
            type: USER_REGISTER_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail
            : error.message,
        })

    }
}


export const getUserDetails = (idOrPage) => async (dispatch, getState) => {

    try {

        // userReducers.js case
        dispatch({
            type: USER_DETAILS_REQUEST
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

        const { data } = await axios.get(
            `http://localhost:8000/api/v1/users/${idOrPage}/`,
            config
        )

        // Get the user data after making the API profile update call. Calls the reducer to update the state.
        dispatch({
            type: USER_DETAILS_SUCCESS,
            payload: data
        })

    }
    catch (error) {

        // Start product reducer with the specified case type
        dispatch({
            type: USER_DETAILS_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail
            : error.message,
        })

    }
}


export const updateUserProfile = (userData) => async (dispatch, getState) => {

    try {

        // userReducers.js case
        dispatch({
            type: USER_UPDATE_PROFILE_REQUEST
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
        const { data } = await axios.put(
            'http://localhost:8000/api/v1/users/profile/update/',
            userData,
            config
        )

        // Get the user data after making the API profile update call. Calls the reducer to update the state.
        dispatch({
            type: USER_UPDATE_PROFILE_SUCCESS,
            payload: data
        })

        // logs the user in with the new updated data. Calls the right reducer.
        dispatch({
            type: USER_LOGIN_SUCCESS,
            payload: data
        })

        // Save the user data to the user's browser local storage after updating
        localStorage.setItem('userInfo', JSON.stringify(data))

    }
    catch (error) {

        // Start product reducer with the specified case type
        dispatch({
            type: USER_UPDATE_PROFILE_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail
            : error.message,
        })

    }
}