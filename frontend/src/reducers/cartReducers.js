// Reducers initiate the state and changes the state according to the actions
// it receives from the actions that were dispatched.


import {
    CART_ADD_ITEM,
    CART_REMOVE_ITEM,
    CART_SAVE_SHIPPING_ADDRESS
} from '../constants/cartConstants'


export const cartReducer = ( state = { cartItems: [], shippingAddress: {} }, action ) => {

    switch(action.type) {

        case CART_ADD_ITEM:
            
            const item = action.payload
            const existItem = state.cartItems.find( (obj) => obj.id === item.id)

            // If item exists
            if (existItem) {

                return {

                    // Returns previous state
                    ...state,

                    // Loop through array and see if a cart item matches the new item. Replace the matching item with the new item.
                    // If the item we got from "item" matches an existing item, only use the new "item" const. If not, return the original.
                    cartItems: state.cartItems.map( (obj) => 
                        obj.id === existItem.id ? item : obj
                    )
                }
            }
            else {

                return {

                    // Returns previous state
                    ...state,

                    // Return original cart items
                    cartItems: [...state.cartItems, item]
                }
            }
        
        case CART_REMOVE_ITEM:

            return {

                ...state,

                // Filter out any items that doesn't match what's in the Redux action object.
                // Returns an array without the deleted item.
                cartItems: state.cartItems.filter( (item) => item.id !== action.payload )
            }

        case CART_SAVE_SHIPPING_ADDRESS:

            return {

                // Returns previous state
                ...state,

                // Add the shippingAddress variable to the state.
                shippingAddress: action.payload
            }

        default:
            return state
    }
}