import React from 'react'
import { Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'     // Using Link instead of the a tag allows loading components of a specific page rather than triggering a full page reload.

import Rating from './Rating'


function Product({ product }) {

    return (

        <Card className="my-3 p-3 rounded">
            <Link to={`/product/${product.id}`}>
                <Card.Img src={product.image} />
            </Link>

            <Card.Body>
                <Link to={`/product/${product.id}`}>
                    <Card.Title as="div">
                        <strong>{product.name}</strong>
                    </Card.Title>
                </Link>

                <Card.Text as="div">
                    <div className="my-3">
                        {product.rating} from {product.numReviews} reviews
                    </div>

                    <Rating value={product.rating} text={`${product.numReviews} reviews`} color={'#f8e825'} />
                </Card.Text>

                <Card.Text as="h3">
                    ${product.price}
                </Card.Text>
            </Card.Body>
        </Card>

    )
}

export default Product
