import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { Form, Button } from 'react-bootstrap'

import FormContainer from '../../components/shared/FormContainer'
import CheckoutSteps from '../../components/cart/CheckoutSteps'

import { saveShippingAddress } from '../../actions/cartActions'


function ShippingScreen({ history }) {

    // Get shipping address from the cart state variable.
    const cart = useSelector( (state) => state.cart )
    const { shippingAddress } = cart

    // Get userLogin variable from the state. Will use to see if the user can access this page.
    const userLogin = useSelector( (state) => state.userLogin )
    const { userInfo } = userLogin

    // dispatch is used to trigger an action
    const dispatch = useDispatch()

    // Initialize the state variables and set the default to whatever the current state is.
    // Pre-populates if the user's state contains the shippingAddress and is not empty.
    const [address, setAddress] = useState(shippingAddress.address)
    const [city, setCity] = useState(shippingAddress.city)
    const [postalCode, setPostalCode] = useState(shippingAddress.postalCode)
    const [country, setCountry] = useState(shippingAddress.country)

    const submitHandler = (event) => {

        event.preventDefault()

        // Saves the user's address to the local storage and updates the state.
        // Will automatically send as a key/value pair.
        dispatch(saveShippingAddress({ address, city, postalCode, country }))

        // Send the customer to the payment page after sending in the shipping address data.
        history.push('/payment')
    }
 
    // Verifies that the user is logged in by checking if their userInfo state variable
    // contains information.
    // Triggers after initial render and when the userInfo state variable changes.
    useEffect( () => {
        
        if (!userInfo) {

            history.push('/login')
        }
    }, [userInfo, history])

    return (

        <FormContainer>

            <CheckoutSteps step1 step2 />

            <h1>Shipping</h1>
            <Form onSubmit={ submitHandler }>

                <Form.Group controlId="address">
                    <Form.Label>Address</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter address"
                        value={address ? address : ''}
                        onChange={ (event) => setAddress(event.target.value) }
                        required
                    >
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="city">
                    <Form.Label>City</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter city"
                        value={city ? city : ''}
                        onChange={ (event) => setCity(event.target.value) }
                        required
                    >
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="postalCode">
                    <Form.Label>Postal Code</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter postal code"
                        value={postalCode ? postalCode : ''}
                        onChange={ (event) => setPostalCode(event.target.value) }
                        required
                    >
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="country">
                    <Form.Label>Country</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter country"
                        value={country ? country : ''}
                        onChange={ (event) => setCountry(event.target.value) }
                        required
                    >
                    </Form.Control>
                </Form.Group>

                <Button type="submit" variant="primary">Continue</Button>

            </Form>
        </FormContainer>

    )
}

export default ShippingScreen
