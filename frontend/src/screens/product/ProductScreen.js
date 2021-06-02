import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Row, Col, Image, ListGroup, Button, Card } from 'react-bootstrap'
import axios from 'axios'

import Rating from '../../components/product/Rating'
import products from '../../products'

import './css/product_screen.css'

function ProductScreen({ match }) {

    const [product, setProduct] = useState([])

    // Use effect triggers when the component loads or a state updates (dictated by the empty array)
    useEffect( () => {

        // Async function to use await
        async function fetchProducts() {

            // Use axios to update state
            const { data } = await axios.get(`http://localhost:8000/api/v1/item/${match.params.id}`)
            setProduct(data)

            console.log('data:', data.image.file)
        }

        // Call function to load all of the products in the API
        fetchProducts()

    }, [])

    // Shows "Still loading..." while the products list is empty. Once all the data is fetched,
    // it will render the page's contents
    if (product.length === 0) {

        return (
            <div> Still loading...</div>
        )

    }
    else {

        return (

            <div>
                <Link to="/" className='btn btn-ligh my-3'>Go Back</Link>
    
                <Row>
                    <Col md={6}>
                        <Image src={product.image.file} alt={product.name} fluid />
                    </Col>
    
                    <Col md={3}>
                        <ListGroup variant="flush">
                            <ListGroup.Item>
                                <h3>{product.name}</h3>
                            </ListGroup.Item>
    
                            <ListGroup.Item>
                                <Rating value={product.rating} text={`${product.numReviews} reviews`} color={'#f8e825'} />
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
                                            {product.countInStock > 0 ? 'In Stock' : 'Out of Stock'}
                                        </Col>
                                    </Row>
                                </ListGroup.Item>
    
                                <ListGroup.Item>
                                    <Button className="add-btn btn-block" disabled={product.countInStock == 0} type="button">Add to Cart</Button>
                                </ListGroup.Item>
                            </ListGroup>
                        </Card>
                    </Col>
                </Row>
            </div>
    
        )

    }

}

export default ProductScreen
