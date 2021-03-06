import React from 'react'
import { Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'     // Using Link instead of the a tag allows loading components of a specific page rather than triggering a full page reload.

import Rating from './Rating'

import './css/product.css'


function Product({ product, classProp }) {

    return (

        <Card className="my-3 p-3 rounded">
            <Link to={`/product/${product.id}`}>
                <Card.Img className={classProp} src={product?.image?.file ?? ""} />
            </Link>

            <Card.Body>
                <Link to={`/product/${product.id}`}>
                    <Card.Title as="div">
                        <strong>{product.title}</strong>
                    </Card.Title>
                </Link>

                <Card.Text as="div">
                    <div className="my-3">
                        {product.rating} from {product.quantity_reviews} reviews
                    </div>

                    <Rating value={product.rating} text={`${product.quantity_reviews} reviews`} color={'#f8e825'} />
                </Card.Text>

                <Card.Text as="h3">
                    ${product.price}
                </Card.Text>
            </Card.Body>
        </Card>

    )
}

export default Product
