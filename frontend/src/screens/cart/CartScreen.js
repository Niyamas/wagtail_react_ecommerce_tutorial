import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col, ListGroup, Image, Form, Button, Card } from 'react-bootstrap'
import Message from '../../components/shared/Message'
import { addToCart, removeFromCart } from '../../actions/cartActions'


function CartScreen({ match, location, history }) {
    // Destructure to get data from browser and url.

    const productId = match.params.id

    // Get parameters in URL. If it exists, get the order item quantity from the URL.
    const quantity = location.search ? Number(location.search.split('=')[1]) : 1

    // dispatch is used to trigger an action
    const dispatch = useDispatch()

    // Pull data from the state (cart item data) and destructure to get the cartItems variable.
    const cart = useSelector( (state) => state.cart )
    const { cartItems } = cart

    useEffect( () => {

        // Only if there's a product Id, will the addToCart action trigger.
        if (productId) {

            // Updates the state and adds the item to the user's local storage on their browser.
            dispatch(addToCart(productId, quantity))
        }

        // Will not trigger when dispatch, productId, or quantity have not changed when states are changed.
    }, [dispatch, productId, quantity])

    //console.log('cartItems:', cartItems)

    // Handles the delete from cart icon.
    const removeFromCartHandler = (id) => {

        // Remove the item with the specified id from the cart via a Redux action.
        dispatch(removeFromCart(id))
    }

    // Handles when the user clicks the available checkout button.
    const checkoutHandler = () => {

        /* If the user is logged in, send them to the shipping page, and if not go to the login page. */
        history.push('/login?redirect=shipping')
    }

    return (

        <Row>
            <Col md={8}>
                <h1>Shopping Cart</h1>

                {
                    cartItems.length === 0 ? (

                        <Message variant="info">
                            Your cart is empty <Link to="/">Go Back</Link>
                        </Message>

                    ) : (

                            <ListGroup variant="flush">

                                {
                                    cartItems.map( (item) => (
                                    
                                        <ListGroup.Item key={ item.id }>
                                            <Row>
                                                <Col md={2}>
                                                    <Image src={ item.image } alt={ item.name } fluid rounded />
                                                </Col>
                                                
                                                <Col md={3}>
                                                    <Link to={`/product/${ item.id }`}>{ item.name }</Link>
                                                </Col>

                                                <Col md={2}>
                                                    ${ Number(item.price) }
                                                </Col>

                                                <Col md={3}>
                                                    <Form.Control
                                                        as="select"
                                                        value={ item.quantity }
                                                        onChange={ (event) => dispatch(addToCart(item.id, Number(event.target.value))) }
                                                    >
                                                        {
                                                            [...Array(item.countInStock).keys()].map( (currentCount) => (
                                                                <option key={currentCount + 1} value={currentCount + 1}>
                                                                    {/* Compensate for the fact that the array starts with 0 */}
                                                                    {currentCount + 1}
                                                                </option>
                                                            ))
                                                        }
                                                    </Form.Control>
                                                </Col>

                                                <Col md={1}>
                                                    <Button
                                                        type="button"
                                                        variant="light"
                                                        onClick={ () => removeFromCartHandler(item.id) }
                                                    >
                                                        <i className="fas fa-trash"></i>
                                                    </Button>
                                                </Col>
                                            </Row>
                                        </ListGroup.Item>
                                    ))
                                }

                            </ListGroup>
                    )
                }
            </Col>

            <Col md={4}>
                <Card>
                    <ListGroup variant="flush">
                        <ListGroup.Item>
                            {/* Add all of the item counts together */}
                            <h2>Subtotal ({ cartItems.reduce( (accumulator, item) => accumulator + item.quantity, 0 ) }) items</h2>

                            ${ cartItems.reduce( (accumulator, item) => accumulator + item.quantity * item.price, 0 ).toFixed(2) }
                        </ListGroup.Item>
                    </ListGroup>

                    <ListGroup>
                        <Button
                            type="button"
                            className="btn-block"
                            disabled={ cartItems.length === 0 }
                            onClick={ checkoutHandler }
                        >
                            Proceed to Checkout
                        </Button>
                    </ListGroup>
                </Card>
            </Col>
        </Row>

    )
}

export default CartScreen
