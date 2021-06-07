// Reducers are functions that tie actions and states together and allows them to interact.

import { 
    USER_LOGIN_REQUEST,
    USER_LOGIN_SUCCESS,
    USER_LOGIN_FAIL,
    USER_LOGOUT
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