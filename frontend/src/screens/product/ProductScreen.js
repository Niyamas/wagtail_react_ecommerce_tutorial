import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Row, Col, Image, ListGroup, Button, Card, Form } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'

import Rating from '../../components/product/Rating'
import Loader from '../../components/shared/Loader'
import Message from '../../components/shared/Message'
import { listProductDetails } from '../../actions/productActions'

import './css/product_screen.css'

// match holds the specific object (item) information
function ProductScreen({ match, history }) {

    const [quantity, setQuantity] = useState(1)

    // A redux hook that dispatches an action. Like setState, but redux
    const dispatch = useDispatch()

    // useSelector hook. Pull from the current state, the productDetails (productDetails is defined in the reducer constant in store.js)
    const productDetails = useSelector( (state) => state.productDetails)

    // Unpack variables from the productDetails state
    const { loading, error, product } = productDetails

    // Use effect triggers when the component loads or a state updates (dictated by the empty array). Triggers after dispatch or match changes.
    useEffect( () => {

        // Initiate the listProductDetails action and pass in the item's id to get the right API URL.
        dispatch(listProductDetails(match.params.id))

    }, [dispatch, match])

    const addToCartHandler = () => {

        // Push to session history. Redirects to the specified URL.
        history.push(`/cart/${match.params.id}?quantity=${quantity}`)
    }


    // Shows "Still loading..." while the products list is empty. Once all the data is fetched,
    // it will render the page's contents
    /* if (product.length === 0) {

        return (
            <div> Still loading...</div>
        )

    }
    else { */

    return (

        <div>
            <Link to="/" className='btn btn-ligh my-3'>Go Back</Link>

            {
                loading ? <Loader /> 
                    : error ? <Message variant='danger'>{error}</Message>
                        : (
                            <Row>
                                <Col md={6}>
                                    <Image src={product?.image?.file ?? ""} alt={product.name} fluid />
                                </Col>
                
                                <Col md={3}>
                                    <ListGroup variant="flush">
                                        <ListGroup.Item>
                                            <h3>{product.title}</h3>
                                        </ListGroup.Item>
                
                                        <ListGroup.Item>
                                            <Rating value={product.rating} text={`${product.quantity_reviews} reviews`} color={'#f8e825'} />
                                        </ListGroup.Item>
                
                                        <ListGroup.Item>
                                            Price: ${product.price}
                                        </ListGroup.Item>
                
                                        <ListGroup.Item dangerouslySetInnerHTML={{ __html: `Description: ${product.description}` }}>
                                        </ListGroup.Item>
                                    </ListGroup>
                                </Col>
                
                                <Col md={3}>
                                    <Card>
                                        <ListGroup variant="flush">
                                            <ListGroup.Item>
                                                <Row>
                                                    <Col>Price:</Col>
                                                    <Col>
                                                        <strong>${product.price}</strong>
                                                    </Col>
                                                </Row>
                                            </ListGroup.Item>
                
                                            <ListGroup.Item>
                                                <Row>
                                                    <Col>Status:</Col>
                                                    <Col>
                                                        {product.quantity_in_stock > 0 ? 'In Stock' : 'Out of Stock'}
                                                    </Col>
                                                </Row>
                                            </ListGroup.Item>

                                            {product.quantity_in_stock > 0 && (
                                                <ListGroup.Item>
                                                    <Row>
                                                        <Col>Qty</Col>
                                                        <Col className='my-1' xs='auto'>
                                                            <Form.Control
                                                                as="select"
                                                                value={quantity}
                                                                onChange={ (e) => setQuantity(e.target.value) }
                                                            >
                                                                {
                                                                    [...Array(product.quantity_in_stock).keys()].map( (currentCount) => (
                                                                        <option key={currentCount + 1} value={currentCount + 1}>
                                                                            {/* Compensate for the fact that the array starts with 0 */}
                                                                            {currentCount + 1}
                                                                        </option>
                                                                    ))
                                                                }
                                                            </Form.Control>
                                                        </Col>
                                                    </Row>
                                                </ListGroup.Item>
                                            )}
                
                                            <ListGroup.Item>
                                                <Button
                                                    className="add-btn btn-block"
                                                    onClick={ addToCartHandler }
                                                    disabled={product.quantity_in_stock == 0}
                                                    type="button"
                                                >
                                                    Add to Cart
                                                </Button>
                                            </ListGroup.Item>
                                        </ListGroup>
                                    </Card>
                                </Col>
                            </Row>
                        )

            }

        </div>

    )

    //}

}

export default ProductScreen
