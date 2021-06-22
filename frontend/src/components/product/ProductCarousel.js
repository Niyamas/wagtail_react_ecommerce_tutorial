import React, { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Link } from 'react-router-dom'
import { Carousel, Image } from 'react-bootstrap'

import Loader from '../shared/Loader'
import Message from '../shared/Message'

import { listTopProducts } from '../../actions/productActions'

import './css/product.css'

function ProductCarousel() {

    const dispatch = useDispatch()

    const productTopRated = useSelector(state => state.productTopRated)
    const { loading, products, error } = productTopRated

    useEffect( () => {

        dispatch(listTopProducts())
    }, [dispatch])

    return (

        loading ? <Loader />
            : error ? <Message variant="danger">{ error }</Message>
            : (
                <Carousel pause="hover" className="bg-dark">
                    {
                        products.map( (product) => (

                            <Carousel.Item key={product.id}>
                                <Link to={`/product/${product.id}/`}>
                                    <Image src={product.image.file} alt={product.title} fluid />
                                    <Carousel.Caption className="carousel.caption">
                                        <h4>{ product.title } (${product.price})</h4>
                                    </Carousel.Caption>
                                </Link>
                            </Carousel.Item>
                        ))
                    }
                </Carousel>
            )


    )
}

export default ProductCarousel
