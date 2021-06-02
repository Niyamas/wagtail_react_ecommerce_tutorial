import React, { useState, useEffect } from 'react'
import { Row, Col } from 'react-bootstrap'
import axios from 'axios'

import products from '../../products'
import Product from '../../components/product/Product'

function HomeScreen() {

    const [products, setProducts] = useState([])

    // Use effect triggers when the component loads or a state updates.
    useEffect( () => {

        // Async function to use await
        async function fetchProducts() {

            // Use axios to update state
            const { data } = await axios.get('http://localhost:8000/api/v1/items/')
            setProducts(data)
        }

        // Call function to load all of the products in the API
        fetchProducts()

    }, [])

    return (

        <div>
            <h1>Latest Products</h1>

            <Row>
                {products.map( product => (
                    <Col key={product.id} sm={12} md={6} lg={4} xl={3}>
                        <Product product={product} />
                    </Col>
                ))}
            </Row>
        </div>

    )
}

export default HomeScreen
