import React, { /* useState, */ useEffect } from 'react'
import { Row, Col } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'

import Product from '../../components/product/Product'
import Paginate from '../../components/product/Paginate'
import ProductCarousel from '../../components/product/ProductCarousel'
import Loader from '../../components/shared/Loader'
import Message from '../../components/shared/Message'
import { listProducts } from '../../actions/productActions'

import './css/home.css'


function HomeScreen({ history }) {

    // A redux hook that dispatches an action. Like setState, but redux
    // dispatch is used to trigger an action
    const dispatch = useDispatch()

    // Chooses the productList from the dictionary of reducers in store.js and other files
    const productList = useSelector( (state) => state.productList)

    // Destructured variables pulled from the state
    const { loading, error, products, page, pages } = productList

    // @ todo: pickup @ 9:30 min mark https://www.udemy.com/course/django-with-react-an-ecommerce-website/learn/lecture/24599974

    let urlParams = history.location.search

    let pageParam = new URLSearchParams(history.location.search).get('page')

    console.log('pageParam =', pageParam)
    console.log('urlParams =', urlParams)

    // Use effect triggers when the component loads or a state updates. (Triggers when dispatch changes)
    useEffect( () => {

        // A redux action defined in productActions.js that fetches the list of items using axios.
        dispatch(listProducts(urlParams))

    }, [dispatch, urlParams])

    return (

        <div>
            {
                /* Only show the carousel when the user isn't searching. */
                (!pageParam || pageParam === '1' || !urlParams) && <ProductCarousel />
            }
            
            <h1 className="latest-products-banner">Latest Products</h1>

            {/* Check first if the items are loading, if not, display error. If it's loaded, display the items */}
            {
                loading ? <Loader />
                    : error ? <Message variant="danger">{error}</Message>
                        : (
                            <div>
                                <Row>
                                    {products.map( product => (
                                        <Col key={product.id} sm={12} md={6} lg={4} xl={3}>
                                            <Product product={product} classProp="home-product-img" />
                                        </Col>
                                    ))}
                                </Row>

                                <Paginate page={page} pages={pages} urlParams={urlParams}/>
                            </div>
                        )
            }


        </div>

    )
}

export default HomeScreen
