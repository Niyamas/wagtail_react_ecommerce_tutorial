// After being dispatched, the action will update the state and do other logic.

import axios from 'axios'
import {
    CART_ADD_ITEM,
    CART_REMOVE_ITEM,
    CART_SAVE_SHIPPING_ADDRESS
} from '../constants/cartConstants'


export const addToCart = (productId, quantity) => async(dispatch, getState) => {
    // getState is like useSelector. Can get parts or all of the state.

    const { data } = await axios.get(`http://localhost:8000/api/v1/item/${productId}`)

    dispatch({
        type: CART_ADD_ITEM,
        payload: {
            id: data.id,
            name: data.title,
            image: data.image.file,
            price: data.price,
            countInStock: data.quantity_in_stock,
            quantity
        }
    })

    // Store item in local storage, so when the user revisits the website, their cart will still be there.
    // Is cart the cartReducer?
    localStorage.setItem('cartItems', JSON.stringify(getState().cart.cartItems))

}

export const removeFromCart = (id) => (dispatch, getState) => {

    dispatch({
        type: CART_REMOVE_ITEM,
        payload: id
    })

    // Update the cartItems variable in local storage after removing the item.
    localStorage.setItem('cartItems', JSON.stringify(getState().cart.cartItems))
}

export const saveShippingAddress = (data) => (dispatch) => {

    dispatch({
        type: CART_SAVE_SHIPPING_ADDRESS,
        payload: data
    })

    // Update the cartItems variable in local storage after removing the item.
    localStorage.setItem('shippingAddress', JSON.stringify(data))
}