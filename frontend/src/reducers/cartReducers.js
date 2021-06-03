import { CART_ADD_ITEM } from '../constants/cartConstants'


export const cartReducer = ( state = {cartItems:[]}, action ) => {

    switch(action.type) {

        case CART_ADD_ITEM:
            
            const item = action.payload
            const existItem = state.cartItems.find(obj => obj.product === item.product)

            // If item exists
            if (existItem) {

                return {

                    ...state,

                    // Loop through array and see if a cart item matches the new item. Replace the matching item with the new item.
                    // If the item we got from "item" matches an existing item, only use the new "item" const. If not, return the original.
                    cartItems: state.cartItems.map(obj => 
                        obj.product === existItem.product ? item : obj
                    )
                }
            }
            else {
                return {

                    // Returns original state
                    ...state,

                    // Return original cart items
                    cartItems: [...state.cartItems, item]
                }
            }

        default:
            return state
    }
}