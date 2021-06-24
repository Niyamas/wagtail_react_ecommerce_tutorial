import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { Form, Button, Col } from 'react-bootstrap'

import FormContainer from '../../components/shared/FormContainer'
import CheckoutSteps from '../../components/cart/CheckoutSteps'

import { savePaymentMethod } from '../../actions/cartActions'


function PaymentScreen({ history }) {

    // Get shipping address from the cart state variable.
    const cart = useSelector( (state) => state.cart )
    const { shippingAddress } = cart

    // If the user doesn't have an address saved, redirect the user to the shipping page.
    if (!shippingAddress.address) {

        history.push('/shipping')
    }

    // dispatch is used to trigger an action
    const dispatch = useDispatch()

    // Initialize some state variables
    const [paymentMethod, setPaymentMethod] = useState('PayPal')

    // Handles when the user submits payment information
    const submitHandler = (event) => {

        event.preventDefault()

        // Save the payment method in the cart as paymentMethod under the cart state variable.
        dispatch(savePaymentMethod(paymentMethod))

        // After entering payment, send user to the next page
        history.push('/place-order')
    }

    return (
        
        <FormContainer>
            <CheckoutSteps step1 step2 step3 />
            
            <Form onSubmit={ submitHandler }>
                <Form.Group>
                    <Form.Label className="payment__legend" as="legend">Select Method</Form.Label>
                    <Col>
                        <Form.Check
                            type="radio"
                            label="PayPal or Credit Card"
                            id="paypal"
                            name="paymentMethod"
                            checked
                            onChange={ (event) => setPaymentMethod(event.target.value) }
                        >

                        </Form.Check>
                    </Col>
                </Form.Group>

                <Button className="btn-conglomerate payment-continue-btn" type="submit" variant="primary">Continue</Button>
            </Form>
            
        </FormContainer>
    )
}

export default PaymentScreen
