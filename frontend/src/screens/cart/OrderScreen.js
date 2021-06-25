import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import { PayPalButton } from 'react-paypal-button-v2'

import { Row, Col, ListGroup, Image } from 'react-bootstrap'

import Message from '../../components/shared/Message'
import Loader from '../../components/shared/Loader'
import { domainURL } from '../../constants/domainConstants'
import { ORDER_PAY_RESET } from '../../constants/orderConstants'

import { getOrderDetails, payOrder } from '../../actions/orderActions'


function PlaceOrderScreen({ match }) {

    // Get the order ID
    const orderId = match.params.id

    // From Redux. Enables action dispatch.
    const dispatch = useDispatch()

    const [sdkReady, setSdkReady] = useState(false)

    // Get order, success, and error variables from orderCreate, which is part of the state.
    const orderDetails = useSelector( (state) => state.orderDetails )
    const { order, loading, error } = orderDetails

    console.log('ORDER = ', order)

    // Get order, success, and error variables from orderCreate, which is part of the state.
    const orderPay = useSelector( (state) => state.orderPay )
    const { loading:loadingPay, success:successPay } = orderPay


    // Calculate the total price of the items only when the data is present from the dispatch.
    if (!loading && !error) {

        // Adds the total cost of all items as an attribute to cart (state variable) that is only available for this page.
        // Tax, shipping, and total prices are not needed since it is loaded into the state.
        order.itemsPrice = order.orders.reduce( (acc, item) => acc + item.price * item.quantity, 0 ).toFixed(2)
    }

    // Paypal Client ID: AWoLzZNHfQUh1jzX99Nvw8nkTjvGdGB0VhqNT1A7hNcrswl426IVeHzIWFzRBaOE7KVUSSrUX8PCd69U
    const addPayPalScript = () => {

        const script = document.createElement('script')
        script.type = 'text/javascript'
        script.src = 'https://www.paypal.com/sdk/js?client-id=AWoLzZNHfQUh1jzX99Nvw8nkTjvGdGB0VhqNT1A7hNcrswl426IVeHzIWFzRBaOE7KVUSSrUX8PCd69U'
        script.async = true

        script.onload = () => {
            setSdkReady(true)
        }

        document.body.appendChild(script)
    }

    //
    useEffect( () => {

        // If order doesn't exist or the order ID in the URl doesn't match
        // what's in the state, get the cart details. (order refers to the cart that was ordered)
        if (!order || order.id !== Number(orderId) || successPay) {

            // Clear the orderPay state variable. 
            dispatch({ type: ORDER_PAY_RESET })

            // Fetch cart details.
            dispatch(getOrderDetails(orderId))
        }
        // Show paypal buttons if the order is not paid.
        else if (!order.is_paid) {

                if (!window.paypal) {

                    addPayPalScript()
                }
                else {
                    setSdkReady(true)
                }
        }

    }, 
        [dispatch, order, orderId, successPay]
        /* [dispatch, successPay] */
    )


    const successPaymentHandler = (paymentResult) => {

        dispatch(payOrder(orderId, paymentResult))
    }






    return loading ? (
        <Loader />
    ) : error ? (
        <Message variant='danger'>{error}</Message>
    ) : (

        <div>
            <h1>Order: {order.id}</h1>
            <Row>
                <Col md={8}>
                    <ListGroup variant="flush">

                        <ListGroup.Item>
                            <h2 className="checkout__banner">Shipping</h2>
                            <p><strong>Name: </strong>{order.user_data.first_name} {order.user_data.last_name}</p>
                            <p><strong>Email: </strong><a href={`mailto:${order.user_data.email}`}>{order.user_data.email}</a></p>
                            <p>
                                <strong>Shipping: </strong>
                                { order.shipping_address_data.address }, { order.shipping_address_data.city }
                                {'  '}
                                { order.shipping_address_data.postalCode },
                                {'  '}
                                { order.shipping_address_data.country }
                            </p>

                            {
                                order.is_delivered ? (
                                    <Message variant='success'>Delivered on on {order.delivered_at.substring(0, 10)}</Message>
                                ) : (
                                    <Message variant='warning'>Not Delivered</Message>
                                )
                            }
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2 className="checkout__banner">Payment Method</h2>
                            <p>
                                <strong>Method: </strong>
                                { order.payment_method }
                            </p>
                            {
                                order.is_paid ? (
                                    <Message variant='success'>Paid on {order.paid_at.substring(0, 10)}</Message>
                                ) : (
                                    <Message variant='warning'>Not paid</Message>
                                )
                            }
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2 className="checkout__banner">Order Items</h2>

                            {
                                order.orders.length === 0 ? <Message variant="info">Your orders are empty</Message>
                                    : (
                                        <ListGroup variant="flush">
                                            { order.orders.map( (item, index) =>(

                                                <ListGroup.Item key={item.id}>
                                                    <Row>
                                                        <Col md={1}>
                                                            <Image src={  item.image } alt={ item.name } fluid rounded />
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
                            <h2 className="checkout__banner">Order Summary</h2>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <Row>
                                <Col>Items:</Col>
                                <Col>${ order.itemsPrice }</Col>
                            </Row>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <Row>
                                <Col>Shipping:</Col>
                                <Col>${ order.shipping_price }</Col>
                            </Row>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <Row>
                                <Col>Tax:</Col>
                                <Col>${ order.tax_price }</Col>
                            </Row>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <Row>
                                <Col>Total:</Col>
                                <Col>${ order.total_price }</Col>
                            </Row>
                        </ListGroup.Item>

                        {
                            !order.is_paid && (
                                <ListGroup.Item className="paypal-bricks">
                                    {
                                        loadingPay && <Loader />
                                    }
                                    {
                                        !sdkReady ? (
                                            <Loader />
                                        ) : (
                                            <PayPalButton 
                                                amount={order.total_price}
                                                onSuccess={successPaymentHandler}
                                                
                                            />
                                        )
                                    }
                                </ListGroup.Item>
                            )
                        }




                        <ListGroup.Item>
                            {
                                error && <Message variant="danger">{ error }</Message>
                            }
                        </ListGroup.Item>

                    </ListGroup>
                </Col>
            </Row>
        </div>

    )
}

export default PlaceOrderScreen
