import axios from 'axios'
import { CART_ADD_ITEM } from '../constants/cartConstants'


export const addToCart = (id, quantity) => async(dispatch, getState) => {
    // getState is like useSelector. Can get parts or all of the state.

    const { data } = await axios.get(`http://localhost:8000/api/v1/item/${id}`)

    dispatch({
        type: CART_ADD_ITEM,
        payload: {
            product: data.id,
            name: data.title,
            image: data.image.file,
            price: data.price,
            countInStock: data.quantity_in_stock,
            quantity
        }
    })

    // Store item in local storage, so when the user revisits the website, their cart will still be there.
    localStorage.setItem('cartItems', JSON.stringify(getState().cart.cartItems))


}