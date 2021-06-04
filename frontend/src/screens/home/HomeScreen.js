import React, { /* useState, */ useEffect } from 'react'
import { Row, Col } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'

import Product from '../../components/product/Product'
import Loader from '../../components/shared/Loader'
import Message from '../../components/shared/Message'
import { listProducts } from '../../actions/productActions'

function HomeScreen() {

    // A redux hook that dispatches an action. Like setState, but redux
    // dispatch is used to trigger an action
    const dispatch = useDispatch()

    // Chooses the productList from the dictionary of reducers in store.js and other files
    const productList = useSelector( (state) => state.productList)

    // Destructured variables pulled from the state
    const { loading, error, products } = productList

    // Use effect triggers when the component loads or a state updates. (Triggers when dispatch changes)
    useEffect( () => {

        // A redux action defined in productActions.js that fetches the list of items using axios.
        dispatch(listProducts())

    }, [dispatch])

    return (

        <div>
            <h1>Latest Products</h1>

            {/* Check first if the items are loading, if not, display error. If it's loaded, display the items */}
            {
                loading ? <Loader />
                    : error ? <Message variant="danger">{error}</Message>
                        : (
                            <Row>
                                {products.map( product => (
                                    <Col key={product.id} sm={12} md={6} lg={4} xl={3}>
                                        <Product product={product} />
                                    </Col>
                                ))}
                            </Row>
                        )
            }


        </div>

    )
}

export default HomeScreen
