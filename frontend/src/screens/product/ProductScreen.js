import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Row, Col, Image, ListGroup, Button, Card, Form } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'

import Rating from '../../components/product/Rating'
import Loader from '../../components/shared/Loader'
import Message from '../../components/shared/Message'
import { listProductDetails, createProductReview } from '../../actions/productActions'

import { PRODUCT_CREATE_REVIEW_RESET } from '../../constants/productConstants'

import './css/product_screen.css'

// match holds the specific object (item) information. Passed from App.js via route
function ProductScreen({ match, history }) {

    const [quantity, setQuantity] = useState(1)

    // Review variables
    const [rating, setRating] = useState(0)
    const [comment, setComment] = useState('')

    // A redux hook that dispatches an action. Like setState, but redux
    // dispatch is used to trigger an action
    const dispatch = useDispatch()

    // useSelector hook. Pull from the current state, the productDetails (productDetails is defined in the reducer constant in store.js)
    // Unpack variables from the productDetails state
    const productDetails = useSelector( (state) => state.productDetails)
    const { loading, error, product } = productDetails

    // Get the logged in user information from their state.
    const userLogin = useSelector( (state) => state.userLogin)
    const { userInfo } = userLogin

    // Get the state variables from the productReviewCreate parent state variable.
    const productReviewCreate = useSelector( (state) => state.productReviewCreate)
    const { loading:loadingProductReview, success:successProductReview, error:errorProductReview } = productReviewCreate

    // Use effect triggers when the component loads or a state updates (dictated by the empty array). Triggers after dispatch or match changes.
    useEffect( () => {

        // After the customer submits a review, reset the rating and comments in
        // the form fields, and clear the productReviewCreate state variable.
        if (successProductReview) {

            setRating(0)
            setComment('')
            dispatch({ type: PRODUCT_CREATE_REVIEW_RESET })
        }

        // Initiate the listProductDetails action and pass in the item's id to get the right API URL.
        dispatch(listProductDetails(match.params.id))

    }, [dispatch, match, successProductReview])

    const addToCartHandler = () => {

        // Push to session history. Redirects to the specified URL.
        history.push(`/cart/${match.params.id}?quantity=${quantity}`)
    }

    const submitHandler = (event) => {

        event.preventDefault()
        
        //
        dispatch(createProductReview(
            match.params.id,
            { rating, comment }
        ))
    }

    return (

        <div>
            <Link to="/" className='go-back-btn btn btn-ligh my-3'>Go Back</Link>

            {
                loading ? <Loader /> 
                    : error ? <Message variant='danger'>{error}</Message>
                        : (
                            <div>
                                <Row>
                                    <Col md={6}>
                                        <Image src={product?.image?.file ?? ""} alt={product.name} fluid />
                                    </Col>
                    
                                    <Col md={3}>
                                        <ListGroup variant="flush">
                                            <ListGroup.Item className="item__detail item__detail--top">
                                                <h3 className="item__title">{product.title}</h3>
                                            </ListGroup.Item>
                    
                                            <ListGroup.Item className="item__detail">
                                                <Rating value={product.rating} text={`${product.quantity_reviews} reviews`} color={'#f8e825'} />
                                            </ListGroup.Item>
                    
                                            <ListGroup.Item className="item__detail">
                                                <span className="item__detail__price"n>Price: </span><span className="item__detail__price__monie">${product.price}</span>
                                            </ListGroup.Item>
                    
                                            <ListGroup.Item className="item__detail item__text" dangerouslySetInnerHTML={{ __html: `<p class="item__description">Description:</p>${product.description}` }}>
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
                                                        className="add-btn btn-block btn-conglomerate"
                                                        onClick={ addToCartHandler }
                                                        disabled={product.quantity_in_stock <= 0 }
                                                        type="button"
                                                    >
                                                        Add to Cart
                                                    </Button>
                                                </ListGroup.Item>
                                            </ListGroup>
                                        </Card>
                                    </Col>
                                </Row>

                                <Row className="reviews">
                                    <Col md={6}>
                                    <h4>Reviews</h4>
                                        {/* @ todo: When pressing ctrl + shift + r on a page with a review, it will say it can't access product.review_data.length */}
                                        { product?.review_data?.length === 0 && <Message variant='info'>No reviews</Message> }

                                        <ListGroup variant="flush">
                                            {
                                                product?.review_data?.map( (review) => (

                                                    <ListGroup.Item className="reviews__review" key={review.id}>
                                                        <strong>{ review.name }</strong>
                                                        <Rating value={ review.rating } color="#f8e825" />
                                                        <p>{ review.created_at.substring(0, 10) }</p>
                                                        <p>{ review.comment }</p>
                                                    </ListGroup.Item>
                                                ))
                                            }
                                            <ListGroup.Item className="reviews__forms">
                                                <h4>Write a review</h4>

                                                { loadingProductReview && <Loader /> }
                                                
                                                { successProductReview && <Message variant="success">Review submitted!</Message> }

                                                { errorProductReview && <Message variant="danger">{errorProductReview}</Message> }

                                                {
                                                    userInfo ? (
                                                        <Form onSubmit={submitHandler}>
                                                            <Form.Group controlId="rating" className="reviews__forms__form">
                                                                <Form.Label>Rating</Form.Label>
                                                                <Form.Control
                                                                    as="select"
                                                                    value={rating}
                                                                    onChange={ (event) => setRating(event.target.value) }
                                                                >
                                                                    <option value="">Select...</option>
                                                                    <option value="1">1 - Poor</option>
                                                                    <option value="2">2 - Fair</option>
                                                                    <option value="3">3 - Good</option>
                                                                    <option value="4">4 - Very Good</option>
                                                                    <option value="5">5 - Excellent</option>
                                                                </Form.Control>
                                                            </Form.Group>

                                                            <Form.Group controlId="comment" className="reviews__forms__form">
                                                                <Form.Label>Review</Form.Label>
                                                                <Form.Control
                                                                    as="textarea"
                                                                    row="5"
                                                                    value={ comment }
                                                                    placeholder="Have a review to share?"
                                                                    onChange={ (event) => setComment(event.target.value) }
                                                                >

                                                                </Form.Control>
                                                            </Form.Group>

                                                            <Button
                                                                disabled={ loadingProductReview }
                                                                type="submit"
                                                                variant="primary"
                                                                className="btn-conglomerate reviews__forms__btn"
                                                            >
                                                                Submit
                                                            </Button>
                                                        </Form>
                                                    ) : (
                                                        <Message variant="info">Please <Link to="/login">Login</Link> to write a review</Message>
                                                    )
                                                }
                                            </ListGroup.Item>
                                        </ListGroup>
                                    </Col>
                                </Row>
                            </div>
                        )

            }

        </div>

    )

    //}

}

export default ProductScreen
