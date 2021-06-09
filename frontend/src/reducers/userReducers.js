// Reducers are functions that tie actions and states together and allows them to interact.

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
    USER_UPDATE_PROFILE_RESET
} from '../constants/userConstants'


export const userLoginReducer = (state = {}, action) => {
    
    // Depending on the action type, do something.
    switch(action.type) {

        // Case when 
        case USER_LOGIN_REQUEST:
            return { loading: true }

        // Case when 
        case USER_LOGIN_SUCCESS:
            return { loading: false, userInfo: action.payload }

        // Case when 
        case USER_LOGIN_FAIL:
            return { loading: false, error: action.payload }

        // Case when 
        case USER_LOGOUT:
            // Resets the state
            return {}

        default:
            return state
    }
}

export const userRegisterReducer = (state = {}, action) => {
    
    // Depending on the action type, do something.
    switch(action.type) {

        // Case when 
        case USER_REGISTER_REQUEST:
            return { loading: true }

        // Case when 
        case USER_REGISTER_SUCCESS:
            return { loading: false, userInfo: action.payload }

        // Case when 
        case USER_REGISTER_FAIL:
            return { loading: false, error: action.payload }

        // Case when 
        case USER_LOGOUT:
            // Resets the state
            return {}

        default:
            return state
    }
}

export const userDetailsReducer = (state = { user: {} }, action) => {
    
    // Depending on the action type, do something.
    switch(action.type) {

        // Case when 
        case USER_DETAILS_REQUEST:
            // ...state, a spread operator, is the initial state
            return { ...state, loading: true }

        // Case when 
        case USER_DETAILS_SUCCESS:
            return { loading: false, user: action.payload }

        // Case when 
        case USER_DETAILS_FAIL:
            return { loading: false, error: action.payload }

        // Case when 
        case USER_DETAILS_RESET:
            return { user: { } }

        default:
            return state
    }
}

export const userUpdateProfileReducer = (state = { }, action) => {
    
    // Depending on the action type, do something.
    switch(action.type) {

        // Case when 
        case USER_UPDATE_PROFILE_REQUEST:
            // ...state, a spread operator, is the initial state
            return { loading: true }

        // Case when 
        case USER_UPDATE_PROFILE_SUCCESS:
            return { loading: false, success: true, userInfo: action.payload }

        // Case when 
        case USER_UPDATE_PROFILE_FAIL:
            return { loading: false, error: action.payload }

        // Case when 
        case USER_UPDATE_PROFILE_RESET:
            return { }

        default:
            return state
    }
}