import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'

import { Form, Button, Row, Col } from 'react-bootstrap'

import Loader from '../../components/shared/Loader'
import Message from '../../components/shared/Message'
import FormContainer from '../../components/shared/FormContainer'

import { login } from '../../actions/userActions'

import './css/user.css'


function LoginScreen({ location, history }) {

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    // A redux hook that dispatches an action. Like setState, but redux
    // dispatch is used to trigger an action
    const dispatch = useDispatch()

    // Get the querystring in the URL parameters and store its value in redirect if possible.
    const redirect = location.search ? location.search.split('=')[1] : '/'
    //console.log('redirect', location)

    // Get userLogin variables from the state.
    const userLogin = useSelector( (state) => state.userLogin )
    const { loading, userInfo, error } = userLogin

    // Trigger state change when history, userInfo, or redirect changes.
    useEffect( () => {

        // If the user is logged in, redirect the user to 
        if (userInfo) {

            history.push(redirect)
        }
    }, [history, userInfo, redirect])

    // Handles when the user clicks the "Sign In" button.
    const submitHandler = (event) => {

        // Prevents the form from being submitted.
        event.preventDefault()

        // Call the login function
        dispatch( login(email, password) )
    }

    return (

        <FormContainer>
            <h1>Sign In</h1>

            { error && <Message variant="danger">{ error }</Message> }

            { loading && <Loader /> }

            <Form onSubmit={ submitHandler }>
                <Form.Group controlId="email" className="login__form">
                    <Form.Label>Email Address</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={ (event) => setEmail(event.target.value) }
                    >
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="password" className="login__form login__form--password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={ (event) => setPassword(event.target.value) }
                    >
                    </Form.Control>
                </Form.Group>

                <Button className="btn-conglomerate" type="submit" variant="primary">Sign In</Button>

            </Form>

            <Row className="py-3">
                <Col>
                    New Customer?&nbsp;
                    <Link
                        /* Check if redirect is there, if not, go to the register page. */
                        to={ redirect ? `/register?redirect=${ redirect }` : '/register' }
                    >
                        Register
                    </Link>
                </Col>
            </Row>

        </FormContainer>

    )
}

export default LoginScreen
