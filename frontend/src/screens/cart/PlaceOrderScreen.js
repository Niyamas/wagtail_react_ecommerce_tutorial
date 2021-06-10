import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link } from 'react-router-dom'

import { Button, Row, Col, ListGroup, Image, Card } from 'react-bootstrap'

import Message from '../../components/shared/Message'
import CheckoutSteps from '../../components/cart/CheckoutSteps'


function PlaceOrderScreen() {

    // Get the cart variable in the list of state variables.
    const cart = useSelector( (state) => state.cart )

    // Adds the total cost of all items as an attribute to cart (state variable) that is only available for this page.
    cart.itemsPrice = cart.cartItems.reduce( (acc, item) => acc + item.price * item.quantity, 0 ).toFixed(2)

    // If the total is over $100, shipping is free. Otherwise, there is a $10 shipping fee
    cart.shippingPrice = (cart.itemsPrice > 100 ? 0 : 10).toFixed(2)

    // Illinois tax rate is 6.25% generally.
    cart.taxPrice = Number((0.0625) * cart.itemsPrice).toFixed(2)

    // Get the grand total for the customer cart.
    cart.totalPrice = ( Number(cart.itemsPrice) + Number(cart.shippingPrice) + Number(cart.taxPrice) ).toFixed(2)

    // Handles the logic after user clicks on the place order button
    const placeOrder = () => {

        console.log('Place order')
    }

    return (

        <div>
            <CheckoutSteps step1 step2 step3 step4 />
            <Row>
                <Col md={8}>
                    <ListGroup variant="flush">

                        <ListGroup.Item>
                            <h2>Shipping</h2>
                            <p>
                                <strong>Shipping: </strong>
                                { cart.shippingAddress.address }, { cart.shippingAddress.city }
                                {'  '}
                                { cart.shippingAddress.postalCode },
                                {'  '}
                                { cart.shippingAddress.country }
                            </p>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2>Payment Method</h2>
                            <p>
                                <strong>Method: </strong>
                                { cart.paymentMethod }
                            </p>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2>Order Items</h2>

                            {
                                cart.cartItems.length === 0 ? <Message variant="info">Your cart is empty</Message>
                                    : (
                                        <ListGroup variant="flush">
                                            { cart.cartItems.map( (item, index) =>(

                                                <ListGroup.Item key={item.id}>
                                                    <Row>
                                                        <Col md={1}>
                                                            <Image src={ item.image } alt={ item.name } fluid rounded />
                                                        </Col>

                                                        <Col>
                                                            <Link to={`/product/${item.id}`}>{ item.name }</Link>
                                                        </Col>

                                                        <Col md={4}>
                                                            { item.quantity } x ${ item.price } = ${ (item.quantity * item.price).toFixed(2) }
                                                        </Col>
                                                    </Row>
                                                </ListGroup.Item>
                                            )) }
                                        </ListGroup>
                                    )
                            }
                            
                        </ListGroup.Item>

                    </ListGroup>
                </Col>

                <Col md={4}>
                    <ListGroup variant="flush">

                        <ListGroup.Item>
                            <h2>Order Summary</h2>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <Row>
                                <Col>Items:</Col>
                                <Col>${ cart.itemsPrice }</Col>
                            </Row>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <Row>
                                <Col>Shipping:</Col>
                                <Col>${ cart.shippingPrice }</Col>
                            </Row>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <Row>
                                <Col>Tax:</Col>
                                <Col>${ cart.taxPrice }</Col>
                            </Row>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <Row>
                                <Col>Total:</Col>
                                <Col>${ cart.totalPrice }</Col>
                            </Row>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <Button
                                type="button"
                                className="btn-block"
                                disabled={ cart.cartItems === 0 }
                                onClick={ placeOrder }
                            >
                                Place Order
                            </Button>
                        </ListGroup.Item>

                    </ListGroup>
                </Col>
            </Row>
        </div>

    )
}

export default PlaceOrderScreen
